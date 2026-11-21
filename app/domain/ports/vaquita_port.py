"""Port interface for Vaquita decentralized liquidity pool."""
from abc import ABC, abstractmethod
from typing import Any, Dict


class VaquitaPort(ABC):
    """
    Hexagonal Port for Vaquita Liquid Staking and Agricultural Lending Pool.
    Manages cooperative liquidity deposits, risk-adjusted reserves, and yield repayments.
    """

    @abstractmethod
    async def get_pool_liquidity(self, pool_id: str) -> Dict[str, Any]:
        """
        Retrieves total, reserved, and available liquidity for the specified pool.
        """
        pass

    @abstractmethod
    async def reserve_liquidity(
        self,
        pool_id: str,
        amount_usdc: float,
        loan_ref: str,
    ) -> Dict[str, Any]:
        """
        Reserves liquidity from the pool for an approved factoring advance.
        """
        pass

    @abstractmethod
    async def release_and_reward(
        self,
        pool_id: str,
        principal_usdc: float,
        yield_usdc: float,
        reservation_id: str,
    ) -> Dict[str, Any]:
        """
        Releases reserved funds and deposits factoring yield back to liquidity providers.
        """
        pass
