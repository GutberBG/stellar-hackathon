"""Port interface for Trustless Work escrow and milestone contracts."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class TrustlessPort(ABC):
    """
    Hexagonal Port for Trustless Work escrow smart contracts.
    Orchestrates milestone-based factoring escrows and programmatic release on harvest delivery.
    """

    @abstractmethod
    async def create_milestone_escrow(
        self,
        borrower_id: int,
        amount_usdc: float,
        milestones: List[Dict[str, Any]],
        loan_code: str,
    ) -> Dict[str, Any]:
        """
        Deploys or creates a milestone escrow contract on Soroban / Trustless Work architecture.
        """
        pass

    @abstractmethod
    async def release_and_repay(
        self,
        escrow_id: str,
        repayment_amount_usdc: float,
        fee_breakdown: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        Executes automated escrow settlement upon harvest verification, returning
        funds + yield to the lending pool and disbursing net balance to the farmer.
        """
        pass
