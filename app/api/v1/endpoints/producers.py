"""Producers API endpoints."""
import time
from typing import List
from fastapi import APIRouter, Depends, status
from app.api.v1.schemas import (
    ProducerResponse,
    ProducerDetailResponse,
    ProducerDeliveryBrief,
    ProducerLoanBrief,
    ProducerCreateRequest,
    ProducerUpdateRequest,
)
from app.api.v1.dependencies import get_producer_repo
from app.infrastructure.repositories import ProducerRepository
from app.infrastructure.orm_models import ProducerORM
from app.core.exceptions import EntityNotFoundException

router = APIRouter()


@router.get("", response_model=List[ProducerResponse], summary="List all registered cacao smallholders")
async def list_producers(
    repo: ProducerRepository = Depends(get_producer_repo),
) -> List[ProducerResponse]:
    """Returns all registered cooperative cacao producers in Alto Beni and Palos Blancos."""
    producers = await repo.get_all()
    return [ProducerResponse.model_validate(p) for p in producers]


@router.post("", response_model=ProducerResponse, status_code=status.HTTP_201_CREATED, summary="Create new cacao producer")
async def create_producer(
    req: ProducerCreateRequest,
    repo: ProducerRepository = Depends(get_producer_repo),
) -> ProducerResponse:
    """Alta directa de productor (usable por Acopiador en campo)."""
    timestamp = int(time.time()) % 100000
    plot_code = req.eudr_plot_code or f"BO-LPZ-AB-{req.community[:4].upper()}-{timestamp:04d}"
    
    orm = ProducerORM(
        name=req.name,
        ci_number=req.ci_number,
        community=req.community,
        cooperative=req.cooperative,
        phone=req.phone,
        eudr_latitude=req.eudr_latitude,
        eudr_longitude=req.eudr_longitude,
        eudr_plot_code=plot_code,
        parcel_hectares=req.parcel_hectares,
        bank_account_hint=req.bank_account_hint,
        compliance_score=0.90,
        risk_tier="BAJO",
        eudr_certified=True,
    )
    saved = await repo.create(orm)
    return ProducerResponse.model_validate(saved)


@router.put("/{producer_id}", response_model=ProducerResponse, summary="Update producer profile and EUDR plot")
async def update_producer(
    producer_id: int,
    req: ProducerUpdateRequest,
    repo: ProducerRepository = Depends(get_producer_repo),
) -> ProducerResponse:
    """Permite al productor actualizar su comunidad, teléfono, cuenta de destino QR y coordenadas/hectáreas."""
    producer = await repo.get_by_id(producer_id)
    if not producer:
        raise EntityNotFoundException("Producer", producer_id)

    if req.name is not None:
        producer.name = req.name
    if req.community is not None:
        producer.community = req.community
    if req.phone is not None:
        producer.phone = req.phone
    if req.bank_account_hint is not None:
        producer.bank_account_hint = req.bank_account_hint
    if req.eudr_latitude is not None:
        producer.eudr_latitude = req.eudr_latitude
    if req.eudr_longitude is not None:
        producer.eudr_longitude = req.eudr_longitude
    if req.parcel_hectares is not None:
        producer.parcel_hectares = req.parcel_hectares

    updated = await repo.update(producer)
    return ProducerResponse.model_validate(updated)


@router.get("/{producer_id}/loans", response_model=List[ProducerLoanBrief], summary="Get producer loans history")
async def get_producer_loans(
    producer_id: int,
    repo: ProducerRepository = Depends(get_producer_repo),
) -> List[ProducerLoanBrief]:
    """Devuelve todos los adelantos (AdvanceLoan) históricos y activos del productor."""
    loans = await repo.get_loans(producer_id)
    return [ProducerLoanBrief.model_validate(loan) for loan in loans]


@router.get("/{producer_id}", response_model=ProducerDetailResponse, summary="Get producer profile and parcel EUDR info")
async def get_producer_detail(
    producer_id: int,
    repo: ProducerRepository = Depends(get_producer_repo),
) -> ProducerDetailResponse:
    """
    Returns producer profile, EUDR (Deforestation Zero) geolocation, parcel code,
    and historical delivery / factoring credit track record.
    """
    producer = await repo.get_by_id(producer_id)
    if not producer:
        raise EntityNotFoundException("Producer", producer_id)

    deliveries_brief = [
        ProducerDeliveryBrief.model_validate(d) for d in producer.deliveries
    ]
    loans_brief = [
        ProducerLoanBrief.model_validate(loan) for loan in producer.loans
    ]

    total_kg = sum(d.net_dry_weight_kg for d in producer.deliveries)

    return ProducerDetailResponse(
        id=producer.id,
        name=producer.name,
        community=producer.community,
        cooperative=producer.cooperative,
        eudr_latitude=producer.eudr_latitude,
        eudr_longitude=producer.eudr_longitude,
        eudr_plot_code=producer.eudr_plot_code,
        phone=producer.phone,
        compliance_score=producer.compliance_score,
        risk_tier=producer.risk_tier,
        hectares=producer.hectares,
        tree_age_years=producer.tree_age_years,
        altitude_m=producer.altitude_m,
        created_at=producer.created_at,
        deliveries_count=len(producer.deliveries),
        total_delivered_kg=round(total_kg, 2),
        deliveries=deliveries_brief,
        active_loans=loans_brief,
    )
