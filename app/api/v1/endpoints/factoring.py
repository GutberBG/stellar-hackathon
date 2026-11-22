"""Factoring & AI Oracle API endpoints."""
import time
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, status
from app.api.v1.schemas import (
    FactoringSimulateRequest,
    FactoringSimulateResponse,
    FactoringExecuteRequest,
    FactoringExecuteResponse,
    FactoringSettleResponse,
)
from app.api.v1.dependencies import (
    get_producer_repo,
    get_loan_repo,
    get_vaquita_adapter,
    get_trustless_adapter,
    get_pollar_adapter,
    get_stellar_adapter,
    get_risk_engine,
    get_settlement_service,
)
from app.infrastructure.repositories import ProducerRepository, LoanRepository
from app.domain.ports.vaquita_port import VaquitaPort
from app.domain.ports.trustless_port import TrustlessPort
from app.domain.ports.pollar_port import PollarPort
from app.domain.ports.stellar_port import StellarPort
from app.ml.risk_engine import RiskEngine
from app.domain.services import SettlementCalculationService
from app.infrastructure.orm_models import AdvanceLoanORM
from app.core.exceptions import EntityNotFoundException, FactoringValidationException, InvalidOperationException
from app.core.config import settings

router = APIRouter()


@router.post(
    "/simulate",
    response_model=FactoringSimulateResponse,
    summary="Simulate agricultural factoring advance with ML risk engine",
)
async def simulate_factoring(
    req: FactoringSimulateRequest,
    producer_repo: ProducerRepository = Depends(get_producer_repo),
    risk_engine: RiskEngine = Depends(get_risk_engine),
) -> FactoringSimulateResponse:
    """
    Simulates credit factoring for a cacao farmer using the RandomForest Risk Engine.
    Considers historical deliveries, compliance score, quality record, and real-time microclimate
    (precipitation in mm and relative humidity %).
    """
    producer = await producer_repo.get_by_id(req.producer_id)
    if not producer:
        raise EntityNotFoundException("Producer", req.producer_id)

    # Calculate historical metrics from past deliveries
    deliveries = producer.deliveries
    if deliveries:
        historical_yield_kg = sum(d.net_dry_weight_kg for d in deliveries) / len(deliveries)
        grade_a_count = sum(1 for d in deliveries if d.quality_grade == "A")
        quality_score = grade_a_count / len(deliveries)
    else:
        historical_yield_kg = 900.0
        quality_score = 0.85

    compliance_rate = producer.compliance_score

    # ML Risk Inference
    ml_result = risk_engine.predict(
        historical_yield_kg=historical_yield_kg,
        compliance_rate=compliance_rate,
        quality_score=quality_score,
        rainfall_mm=req.rainfall_mm,
        humidity_pct=req.humidity_pct,
        expected_harvest_kg=req.expected_harvest_kg,
        base_price_usdc=settings.BASE_CACAO_PRICE_USDC_PER_KG,
        exchange_rate_bob=settings.EXCHANGE_RATE_USDC_BOB,
    )

    return FactoringSimulateResponse(
        producer_id=producer.id,
        producer_name=producer.name,
        community=producer.community,
        cooperative=producer.cooperative,
        expected_harvest_kg=req.expected_harvest_kg,
        risk_score=ml_result["risk_score"],
        risk_level=ml_result["risk_level"],
        approved_advance_pct=ml_result["approved_advance_pct"],
        estimated_harvest_value_usdc=ml_result["estimated_harvest_value_usdc"],
        max_advance_usdc=ml_result["max_advance_usdc"],
        max_advance_bob=ml_result["max_advance_bob"],
        risk_factors=ml_result["risk_factors"],
    )


@router.post(
    "/execute",
    response_model=FactoringExecuteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Execute factoring advance: Vaquita Reserve -> Trustless Escrow -> Pollar QR",
)
async def execute_factoring(
    req: FactoringExecuteRequest,
    producer_repo: ProducerRepository = Depends(get_producer_repo),
    loan_repo: LoanRepository = Depends(get_loan_repo),
    vaquita_port: VaquitaPort = Depends(get_vaquita_adapter),
    trustless_port: TrustlessPort = Depends(get_trustless_adapter),
    pollar_port: PollarPort = Depends(get_pollar_adapter),
    stellar_port: StellarPort = Depends(get_stellar_adapter),
    risk_engine: RiskEngine = Depends(get_risk_engine),
) -> FactoringExecuteResponse:
    """
    Executes an approved factoring advance:
    1. Validates credit capacity with ML risk engine.
    2. Reserves liquidity in Vaquita Pool.
    3. Deploys/Registers milestone escrow via Trustless Work.
    4. Disburses Bolivianos via Pollar Simple QR.
    5. Persists loan in ACTIVE_ESCROW state.
    """
    producer = await producer_repo.get_by_id(req.producer_id)
    if not producer:
        raise EntityNotFoundException("Producer", req.producer_id)

    # 1. Validation with ML Engine
    deliveries = producer.deliveries
    if deliveries:
        historical_yield_kg = sum(d.net_dry_weight_kg for d in deliveries) / len(deliveries)
        grade_a_count = sum(1 for d in deliveries if d.quality_grade == "A")
        quality_score = grade_a_count / len(deliveries)
    else:
        historical_yield_kg = 900.0
        quality_score = 0.85

    ml_result = risk_engine.predict(
        historical_yield_kg=historical_yield_kg,
        compliance_rate=producer.compliance_score,
        quality_score=quality_score,
        rainfall_mm=req.rainfall_mm,
        humidity_pct=req.humidity_pct,
        expected_harvest_kg=req.expected_harvest_kg,
        base_price_usdc=settings.BASE_CACAO_PRICE_USDC_PER_KG,
        exchange_rate_bob=settings.EXCHANGE_RATE_USDC_BOB,
    )

    if req.requested_amount_usdc > ml_result["max_advance_usdc"]:
        raise FactoringValidationException(
            f"El monto solicitado (${req.requested_amount_usdc:,.2f} USDC) excede el máximo pre-aprobado "
            f"(${ml_result['max_advance_usdc']:,.2f} USDC) según evaluación climática y crediticia.",
            details={
                "requested_usdc": req.requested_amount_usdc,
                "max_approved_usdc": ml_result["max_advance_usdc"],
                "risk_score": ml_result["risk_score"],
            },
        )

    # 2. Financial amounts
    approved_amount_usdc = req.requested_amount_usdc
    amount_bob = round(approved_amount_usdc * settings.EXCHANGE_RATE_USDC_BOB, 2)
    timestamp = int(time.time())
    loan_code = f"LOAN-AB-{producer.id}-{timestamp % 1000000}"

    # Step 1: Vaquita Pool Liquidity Reservation
    vaq_res = await vaquita_port.reserve_liquidity(
        pool_id=settings.VAQUITA_POOL_ID,
        amount_usdc=approved_amount_usdc,
        loan_ref=loan_code,
    )

    # Step 2: Trustless Work Milestone Escrow
    milestones = [
        {"milestone_name": "INSPECCION_FLORACION_PODA", "percentage": 30.0, "status": "VERIFIED"},
        {"milestone_name": "ACOPIO_ENTREGA_COSECHA", "percentage": 70.0, "status": "PENDING"},
    ]
    trustless_escrow = await trustless_port.create_milestone_escrow(
        borrower_id=producer.id,
        amount_usdc=approved_amount_usdc,
        milestones=milestones,
        loan_code=loan_code,
    )

    # Step 3: Pollar QR Cash-Out in Bolivianos (BOB)
    pollar_payout = await pollar_port.disburse_to_qr(
        producer_id=producer.id,
        producer_phone=producer.phone,
        amount_bob=amount_bob,
        concept=f"Adelanto Factoring Cacao {loan_code}",
    )

    # Step 3b: Optional real Stellar Testnet transfer to connected Pollar wallet
    stellar_tx_hash: Optional[str] = None
    if req.pollar_wallet_address:
        try:
            demo_xlm = round(min(max(approved_amount_usdc / 100.0, 2.0), 50.0), 2)
            tx_res = await stellar_port.transfer_usdc(
                destination_account=req.pollar_wallet_address,
                amount_usdc=demo_xlm,
                memo=loan_code,
            )
            stellar_tx_hash = tx_res.get("tx_hash")
        except Exception:
            stellar_tx_hash = None

    # Step 4: Persist in Database
    loan_orm = AdvanceLoanORM(
        loan_code=loan_code,
        producer_id=producer.id,
        requested_amount_usdc=req.requested_amount_usdc,
        approved_amount_usdc=approved_amount_usdc,
        amount_bob=amount_bob,
        risk_score=ml_result["risk_score"],
        risk_level=ml_result["risk_level"].value,
        vaquita_reservation_id=vaq_res["reservation_id"],
        trustless_escrow_id=trustless_escrow["escrow_id"],
        pollar_payout_id=pollar_payout["payout_id"],
        pollar_qr_payload=pollar_payout["qr_payload"],
        status="ACTIVE_ESCROW",
    )
    saved_loan = await loan_repo.create(loan_orm)

    return FactoringExecuteResponse(
        loan_id=saved_loan.id,
        loan_code=saved_loan.loan_code,
        producer_id=producer.id,
        producer_name=producer.name,
        requested_amount_usdc=saved_loan.requested_amount_usdc,
        approved_amount_usdc=saved_loan.approved_amount_usdc,
        amount_bob=saved_loan.amount_bob,
        risk_score=saved_loan.risk_score,
        risk_level=ml_result["risk_level"],
        status=saved_loan.status,
        vaquita_reservation_id=saved_loan.vaquita_reservation_id,
        trustless_escrow_id=saved_loan.trustless_escrow_id,
        pollar_payout_id=saved_loan.pollar_payout_id,
        pollar_qr_payload=saved_loan.pollar_qr_payload,
        qr_deep_link=pollar_payout["qr_deep_link"],
        stellar_tx_hash=stellar_tx_hash,
        created_at=saved_loan.created_at,
    )


@router.post(
    "/{loan_id}/settle",
    response_model=FactoringSettleResponse,
    summary="Settle factoring loan upon harvest delivery: Escrow release and 2.5% fee distribution",
)
async def settle_factoring(
    loan_id: int,
    loan_repo: LoanRepository = Depends(get_loan_repo),
    vaquita_port: VaquitaPort = Depends(get_vaquita_adapter),
    trustless_port: TrustlessPort = Depends(get_trustless_adapter),
    calc_service: type[SettlementCalculationService] = Depends(get_settlement_service),
) -> FactoringSettleResponse:
    """
    Settles an active factoring loan when harvest is delivered:
    - Calculates 2.5% commission (2.0% Vaquita Pool yield, 0.5% Ayni Cacao fee).
    - Releases Trustless Work escrow smart contract.
    - Repays principal and credits yield to Vaquita Pool.
    - Marks loan as SETTLED.
    """
    loan = await loan_repo.get_by_id(loan_id)
    if not loan:
        raise EntityNotFoundException("AdvanceLoan", loan_id)

    if loan.status != "ACTIVE_ESCROW":
        raise InvalidOperationException(
            f"El préstamo {loan.loan_code} no puede liquidarse porque su estado actual es '{loan.status}'."
        )

    # 1. Calculate 2.5% fee breakdown
    fee_vaquita, fee_ayni, total_settled = calc_service.calculate_settlement(
        principal_usdc=loan.approved_amount_usdc,
        vaquita_fee_pct=settings.VAQUITA_COMMISSION_PCT,
        ayni_fee_pct=settings.AYNI_COMMISSION_PCT,
    )

    # 2. Release Trustless Work Escrow
    fee_breakdown = {
        "vaquita_pool_yield_usdc": fee_vaquita,
        "ayni_cacao_fee_usdc": fee_ayni,
    }
    settle_receipt = await trustless_port.release_and_repay(
        escrow_id=loan.trustless_escrow_id,
        repayment_amount_usdc=total_settled,
        fee_breakdown=fee_breakdown,
    )

    # 3. Replenish Vaquita Pool and credit 2% yield
    await vaquita_port.release_and_reward(
        pool_id=settings.VAQUITA_POOL_ID,
        principal_usdc=loan.approved_amount_usdc,
        yield_usdc=fee_vaquita,
        reservation_id=loan.vaquita_reservation_id,
    )

    # 4. Update database loan state
    loan.status = "SETTLED"
    loan.fee_vaquita_usdc = fee_vaquita
    loan.fee_ayni_usdc = fee_ayni
    loan.settled_at = datetime.now(timezone.utc)
    await loan_repo.update(loan)

    return FactoringSettleResponse(
        loan_id=loan.id,
        loan_code=loan.loan_code,
        status="SETTLED",
        principal_usdc=loan.approved_amount_usdc,
        fee_vaquita_usdc=fee_vaquita,
        fee_ayni_usdc=fee_ayni,
        total_settled_usdc=total_settled,
        trustless_settlement_tx=settle_receipt["settlement_tx"],
        settled_at=loan.settled_at,
        message="Préstamo liquidado con éxito. Capital y 2% de rendimiento devueltos al Vaquita Pool.",
    )
