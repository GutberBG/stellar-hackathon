"""Mock adapter for Trustless Work milestone escrow smart contracts."""
import hashlib
import time
from typing import Any, Dict, List
from app.domain.ports.trustless_port import TrustlessPort


class MockTrustlessAdapter(TrustlessPort):
    """
    Simulated implementation of Trustless Work escrow smart contracts on Soroban.
    Manages condition-based releases tied to harvest delivery milestones.

    # TODO: Integrar SDK real de Trustless Work (Trustless Work Escrow Smart Contracts)
    # Ejemplo de migración futura:
    # from trustless_work_sdk import EscrowClient
    # escrow_client = EscrowClient(factory_address=settings.TRUSTLESS_WORK_ESCROW_FACTORY)
    """

    async def create_milestone_escrow(
        self,
        borrower_id: int,
        amount_usdc: float,
        milestones: List[Dict[str, Any]],
        loan_code: str,
    ) -> Dict[str, Any]:
        """
        Simulates deployment of a multi-sig milestone escrow contract.
        """
        timestamp = int(time.time())
        seed = f"TRUSTLESS_ESCROW:{loan_code}:{borrower_id}:{amount_usdc}:{timestamp}"
        escrow_id = "escrow_tw_" + hashlib.sha256(seed.encode()).hexdigest()[:16]
        contract_address = "CBH" + hashlib.sha256(f"CONTRACT:{escrow_id}".encode()).hexdigest().upper()[:53]

        return {
            "status": "ACTIVE_ESCROW",
            "escrow_id": escrow_id,
            "contract_address": contract_address,
            "loan_code": loan_code,
            "amount_usdc": amount_usdc,
            "borrower_id": borrower_id,
            "arbiter": "GCOOPERATIVAELCEIBOARBITER9999999999999999999999999999999",
            "milestones": milestones,
            "created_at": timestamp,
        }

    async def release_and_repay(
        self,
        escrow_id: str,
        repayment_amount_usdc: float,
        fee_breakdown: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        Simulates programmatic escrow execution, transferring principal + yields back
        to Vaquita Pool and Ayni Cacao, and unlocking collateral.
        """
        timestamp = int(time.time())
        settle_seed = f"TRUSTLESS_SETTLE:{escrow_id}:{repayment_amount_usdc}:{timestamp}"
        settlement_tx = hashlib.sha256(settle_seed.encode()).hexdigest()

        return {
            "status": "SETTLED",
            "escrow_id": escrow_id,
            "settlement_tx": settlement_tx,
            "repayment_amount_usdc": repayment_amount_usdc,
            "fee_breakdown": fee_breakdown,
            "settled_at": timestamp,
        }
