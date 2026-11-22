"""Producers API endpoints."""
from typing import List
from fastapi import APIRouter, Depends
from app.api.v1.schemas import ProducerResponse, ProducerDetailResponse, ProducerDeliveryBrief, ProducerLoanBrief
from app.api.v1.dependencies import get_producer_repo
from app.infrastructure.repositories import ProducerRepository
from app.core.exceptions import EntityNotFoundException

router = APIRouter()


@router.get("", response_model=List[ProducerResponse], summary="List all registered cacao smallholders")
async def list_producers(
    repo: ProducerRepository = Depends(get_producer_repo),
) -> List[ProducerResponse]:
    """Returns all registered cooperative cacao producers in Alto Beni and Palos Blancos."""
    producers = await repo.get_all()
    return [ProducerResponse.model_validate(p) for p in producers]


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
