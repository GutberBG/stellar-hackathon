"""Deliveries (Acopio & Boleta Transparente) API endpoints."""
import time
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from app.api.v1.schemas import DeliveryCreateRequest, DeliveryResponse, DeliveryListResponse
from app.api.v1.dependencies import (
    get_delivery_repo,
    get_producer_repo,
    get_stellar_adapter,
    get_delivery_service,
)
from app.infrastructure.repositories import DeliveryRepository, ProducerRepository
from app.domain.ports.stellar_port import StellarPort
from app.domain.services import DeliveryCalculationService
from app.infrastructure.orm_models import HarvestDeliveryORM
from app.core.exceptions import EntityNotFoundException
from app.core.config import settings

router = APIRouter()


@router.post(
    "",
    response_model=DeliveryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register transparent collection receipt (Boleta Transparente)",
)
async def create_delivery(
    req: DeliveryCreateRequest,
    delivery_repo: DeliveryRepository = Depends(get_delivery_repo),
    producer_repo: ProducerRepository = Depends(get_producer_repo),
    stellar_port: StellarPort = Depends(get_stellar_adapter),
    calc_service: type[DeliveryCalculationService] = Depends(get_delivery_service),
) -> DeliveryResponse:
    """
    Registers a new cacao delivery at the collection station (acopio).
    Applies agronomic business rules:
    - BABA: 0.33 dry conversion factor.
    - SECO: moisture penalty if > 7.5%.
    - Grade multiplier: A (1.0x), B (0.90x), C (0.75x).
    Generates SHA-256 hash with EUDR coordinates and notarizes on Stellar ledger.
    """
    producer = await producer_repo.get_by_id(req.producer_id)
    if not producer:
        raise EntityNotFoundException("Producer", req.producer_id)

    # 1. Agronomic dry weight calculation
    net_dry_weight_kg, penalty_kg = calc_service.calculate_net_dry_weight(
        cacao_type=req.cacao_type,
        gross_weight_kg=req.gross_weight_kg,
        moisture_percentage=req.moisture_percentage,
    )

    # 2. Pricing and Bolivian currency conversion
    final_price_usdc, total_amount_usdc, total_amount_bob = calc_service.calculate_price_and_totals(
        net_dry_weight_kg=net_dry_weight_kg,
        base_price_usdc=req.base_price_per_kg_usdc,
        quality_grade=req.quality_grade,
        exchange_rate_bob=settings.EXCHANGE_RATE_USDC_BOB,
    )

    # 3. Unique delivery tracking code
    timestamp = int(time.time())
    delivery_code = f"REC-AB-{producer.id}-{timestamp % 1000000}"
    eudr_coords = f"{producer.eudr_latitude},{producer.eudr_longitude}|PLOT:{producer.eudr_plot_code}"

    # 4. Canonical payload hashing (Boleta Transparente + EUDR)
    payload_data = {
        "delivery_code": delivery_code,
        "producer_id": producer.id,
        "producer_name": producer.name,
        "cacao_type": req.cacao_type.value,
        "gross_weight_kg": req.gross_weight_kg,
        "moisture_percentage": req.moisture_percentage,
        "net_dry_weight_kg": net_dry_weight_kg,
        "quality_grade": req.quality_grade.value,
        "final_price_per_kg_usdc": final_price_usdc,
        "total_amount_usdc": total_amount_usdc,
        "total_amount_bob": total_amount_bob,
    }
    payload_hash = calc_service.generate_delivery_hash(payload_data, eudr_coords)

    # 5. On-chain Notarization via Stellar Port (Mock)
    notarization = await stellar_port.notarize_delivery(
        delivery_hash=payload_hash,
        metadata={"delivery_code": delivery_code, "producer": producer.name},
    )

    # 6. Database persistence
    delivery_orm = HarvestDeliveryORM(
        delivery_code=delivery_code,
        producer_id=producer.id,
        cacao_type=req.cacao_type.value,
        gross_weight_kg=req.gross_weight_kg,
        moisture_percentage=req.moisture_percentage,
        net_dry_weight_kg=net_dry_weight_kg,
        quality_grade=req.quality_grade.value,
        base_price_per_kg_usdc=req.base_price_per_kg_usdc,
        final_price_per_kg_usdc=final_price_usdc,
        total_amount_usdc=total_amount_usdc,
        total_amount_bob=total_amount_bob,
        eudr_coords=eudr_coords,
        payload_hash=payload_hash,
        stellar_tx_hash=notarization.get("tx_hash"),
        status="NOTARIZED",
    )
    saved = await delivery_repo.create(delivery_orm)

    response = DeliveryResponse.model_validate(saved)
    response.producer_name = producer.name
    return response


@router.get("", response_model=DeliveryListResponse, summary="List collection receipts with pagination")
async def list_deliveries(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    delivery_repo: DeliveryRepository = Depends(get_delivery_repo),
) -> DeliveryListResponse:
    total = await delivery_repo.count()
    items_orm = await delivery_repo.get_all(limit=limit, offset=offset)

    items: List[DeliveryResponse] = []
    for d in items_orm:
        resp = DeliveryResponse.model_validate(d)
        if d.producer:
            resp.producer_name = d.producer.name
        items.append(resp)

    return DeliveryListResponse(total=total, items=items)


@router.get("/{delivery_id}", response_model=DeliveryResponse, summary="Get collection receipt by ID")
async def get_delivery(
    delivery_id: int,
    delivery_repo: DeliveryRepository = Depends(get_delivery_repo),
) -> DeliveryResponse:
    delivery = await delivery_repo.get_by_id(delivery_id)
    if not delivery:
        raise EntityNotFoundException("HarvestDelivery", delivery_id)

    resp = DeliveryResponse.model_validate(delivery)
    if delivery.producer:
        resp.producer_name = delivery.producer.name
    return resp
