"""Dashboard & Operational Metrics API endpoints."""
from typing import List
from fastapi import APIRouter, Depends
from app.api.v1.schemas import DashboardResponse, PoolStatusResponse, DeliveryResponse, LoanSummaryResponse
from app.api.v1.dependencies import (
    get_pool_repo,
    get_loan_repo,
    get_delivery_repo,
    get_vaquita_adapter,
)
from app.infrastructure.repositories import PoolRepository, LoanRepository, DeliveryRepository
from app.domain.ports.vaquita_port import VaquitaPort
from app.core.config import settings

router = APIRouter()


@router.get("", response_model=DashboardResponse, summary="Get operational dashboard and Vaquita pool status")
async def get_dashboard(
    pool_repo: PoolRepository = Depends(get_pool_repo),
    loan_repo: LoanRepository = Depends(get_loan_repo),
    delivery_repo: DeliveryRepository = Depends(get_delivery_repo),
    vaquita_port: VaquitaPort = Depends(get_vaquita_adapter),
) -> DashboardResponse:
    """
    Returns real-time operational metrics:
    - Vaquita Pool available, reserved, and total liquidity.
    - Total funds advanced in USDC and Bolivianos (Bs.).
    - Active loans in escrow and settled loans count.
    - Latest notarized collection receipts.
    """
    # Ensure pool exists in database
    await pool_repo.ensure_pool(
        settings.VAQUITA_POOL_ID,
        settings.VAQUITA_POOL_INITIAL_LIQUIDITY_USDC,
    )

    # Liquidity info via Vaquita Port
    liquidity_data = await vaquita_port.get_pool_liquidity(settings.VAQUITA_POOL_ID)
    pool_status = PoolStatusResponse(
        pool_id=liquidity_data["pool_id"],
        total_liquidity_usdc=liquidity_data["total_liquidity_usdc"],
        reserved_liquidity_usdc=liquidity_data["reserved_liquidity_usdc"],
        available_liquidity_usdc=liquidity_data["available_liquidity_usdc"],
    )

    # Loan aggregates
    active_loans_count = await loan_repo.count_active()
    settled_loans_count = await loan_repo.count_settled()
    total_advanced_usdc = await loan_repo.get_total_advanced_usdc()
    total_advanced_bob = round(total_advanced_usdc * settings.EXCHANGE_RATE_USDC_BOB, 2)

    # Deliveries count and latest 5
    total_deliveries_count = await delivery_repo.count()
    recent_deliveries_orm = await delivery_repo.get_latest(limit=5)
    recent_deliveries: List[DeliveryResponse] = []
    for d in recent_deliveries_orm:
        resp = DeliveryResponse.model_validate(d)
        if d.producer:
            resp.producer_name = d.producer.name
        recent_deliveries.append(resp)

    # Active loans list
    active_loans_orm = await loan_repo.get_active()
    active_loans: List[LoanSummaryResponse] = []
    for l in active_loans_orm:
        resp = LoanSummaryResponse.model_validate(l)
        if l.producer:
            resp.producer_name = l.producer.name
        active_loans.append(resp)

    return DashboardResponse(
        vaquita_pool=pool_status,
        total_advanced_usdc=total_advanced_usdc,
        total_advanced_bob=total_advanced_bob,
        active_loans_count=active_loans_count,
        settled_loans_count=settled_loans_count,
        total_deliveries_count=total_deliveries_count,
        recent_deliveries=recent_deliveries,
        active_loans=active_loans,
    )
