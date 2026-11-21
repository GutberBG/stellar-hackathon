"""Mock adapter for Vaquita decentralized liquidity pool."""
import hashlib
import time
from typing import Any, Dict
from app.domain.ports.vaquita_port import VaquitaPort
from app.infrastructure.repositories import PoolRepository


class MockVaquitaAdapter(VaquitaPort):
    """
    Simulated implementation of Vaquita Liquid Staking and Agricultural Lending Pool.
    Maintains persistent liquidity state in the database and computes yields.

    # TODO: Integrar SDK real de Vaquita (Vaquita Liquid Staking & Yield Protocol)
    # Ejemplo de migración futura:
    # from vaquita_sdk import VaquitaPoolClient
    # client = VaquitaPoolClient(pool_contract_id=settings.VAQUITA_POOL_ID)
    """

    def __init__(self, pool_repo: PoolRepository):
        self.pool_repo = pool_repo

    async def get_pool_liquidity(self, pool_id: str) -> Dict[str, Any]:
        pool = await self.pool_repo.get_pool(pool_id)
        if not pool:
            return {
                "pool_id": pool_id,
                "total_liquidity_usdc": 0.0,
                "reserved_liquidity_usdc": 0.0,
                "available_liquidity_usdc": 0.0,
            }

        available = round(pool.total_liquidity_usdc - pool.reserved_liquidity_usdc, 2)
        return {
            "pool_id": pool.id,
            "total_liquidity_usdc": pool.total_liquidity_usdc,
            "reserved_liquidity_usdc": pool.reserved_liquidity_usdc,
            "available_liquidity_usdc": max(0.0, available),
        }

    async def reserve_liquidity(
        self,
        pool_id: str,
        amount_usdc: float,
        loan_ref: str,
    ) -> Dict[str, Any]:
        """
        Atomically locks pool capital for a factoring advance.
        """
        pool = await self.pool_repo.reserve_liquidity(pool_id, amount_usdc)
        timestamp = int(time.time())
        res_seed = f"VAQUITA_RES:{pool_id}:{loan_ref}:{timestamp}"
        reservation_id = "vaq_res_" + hashlib.sha256(res_seed.encode()).hexdigest()[:16]

        return {
            "reservation_id": reservation_id,
            "pool_id": pool_id,
            "amount_reserved_usdc": amount_usdc,
            "status": "RESERVED",
            "available_liquidity_usdc": round(pool.total_liquidity_usdc - pool.reserved_liquidity_usdc, 2),
            "reserved_at": timestamp,
        }

    async def release_and_reward(
        self,
        pool_id: str,
        principal_usdc: float,
        yield_usdc: float,
        reservation_id: str,
    ) -> Dict[str, Any]:
        """
        Releases reserved capital upon loan settlement and deposits the 2% Vaquita yield into the pool.
        """
        pool = await self.pool_repo.release_and_reward(pool_id, principal_usdc, yield_usdc)
        return {
            "status": "REPAID_WITH_YIELD",
            "reservation_id": reservation_id,
            "principal_returned_usdc": principal_usdc,
            "yield_earned_usdc": yield_usdc,
            "new_total_liquidity_usdc": pool.total_liquidity_usdc,
            "available_liquidity_usdc": round(pool.total_liquidity_usdc - pool.reserved_liquidity_usdc, 2),
        }
