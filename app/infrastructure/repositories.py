"""Repositories for database persistence following Clean Architecture."""
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.infrastructure.orm_models import ProducerORM, HarvestDeliveryORM, AdvanceLoanORM, VaquitaPoolORM
from app.core.exceptions import EntityNotFoundException, InsufficientLiquidityException


class ProducerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[ProducerORM]:
        result = await self.session.execute(
            select(ProducerORM).order_by(ProducerORM.id.asc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, producer_id: int) -> Optional[ProducerORM]:
        result = await self.session.execute(
            select(ProducerORM)
            .options(selectinload(ProducerORM.deliveries), selectinload(ProducerORM.loans))
            .where(ProducerORM.id == producer_id)
        )
        return result.scalar_one_or_none()

    async def create(self, producer: ProducerORM) -> ProducerORM:
        self.session.add(producer)
        await self.session.commit()
        await self.session.refresh(producer)
        return producer

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(ProducerORM.id)))
        return result.scalar_one() or 0


class DeliveryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, limit: int = 50, offset: int = 0) -> List[HarvestDeliveryORM]:
        result = await self.session.execute(
            select(HarvestDeliveryORM)
            .options(selectinload(HarvestDeliveryORM.producer))
            .order_by(desc(HarvestDeliveryORM.created_at))
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_id(self, delivery_id: int) -> Optional[HarvestDeliveryORM]:
        result = await self.session.execute(
            select(HarvestDeliveryORM)
            .options(selectinload(HarvestDeliveryORM.producer))
            .where(HarvestDeliveryORM.id == delivery_id)
        )
        return result.scalar_one_or_none()

    async def get_by_producer(self, producer_id: int) -> List[HarvestDeliveryORM]:
        result = await self.session.execute(
            select(HarvestDeliveryORM)
            .where(HarvestDeliveryORM.producer_id == producer_id)
            .order_by(desc(HarvestDeliveryORM.created_at))
        )
        return list(result.scalars().all())

    async def get_latest(self, limit: int = 5) -> List[HarvestDeliveryORM]:
        result = await self.session.execute(
            select(HarvestDeliveryORM)
            .options(selectinload(HarvestDeliveryORM.producer))
            .order_by(desc(HarvestDeliveryORM.created_at))
            .limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, delivery: HarvestDeliveryORM) -> HarvestDeliveryORM:
        self.session.add(delivery)
        await self.session.commit()
        await self.session.refresh(delivery)
        return delivery

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(HarvestDeliveryORM.id)))
        return result.scalar_one() or 0


class LoanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[AdvanceLoanORM]:
        result = await self.session.execute(
            select(AdvanceLoanORM)
            .options(selectinload(AdvanceLoanORM.producer))
            .order_by(desc(AdvanceLoanORM.created_at))
        )
        return list(result.scalars().all())

    async def get_by_id(self, loan_id: int) -> Optional[AdvanceLoanORM]:
        result = await self.session.execute(
            select(AdvanceLoanORM)
            .options(selectinload(AdvanceLoanORM.producer))
            .where(AdvanceLoanORM.id == loan_id)
        )
        return result.scalar_one_or_none()

    async def get_active(self) -> List[AdvanceLoanORM]:
        result = await self.session.execute(
            select(AdvanceLoanORM)
            .options(selectinload(AdvanceLoanORM.producer))
            .where(AdvanceLoanORM.status == "ACTIVE_ESCROW")
            .order_by(desc(AdvanceLoanORM.created_at))
        )
        return list(result.scalars().all())

    async def count_active(self) -> int:
        result = await self.session.execute(
            select(func.count(AdvanceLoanORM.id)).where(AdvanceLoanORM.status == "ACTIVE_ESCROW")
        )
        return result.scalar_one() or 0

    async def count_settled(self) -> int:
        result = await self.session.execute(
            select(func.count(AdvanceLoanORM.id)).where(AdvanceLoanORM.status == "SETTLED")
        )
        return result.scalar_one() or 0

    async def get_total_advanced_usdc(self) -> float:
        result = await self.session.execute(
            select(func.sum(AdvanceLoanORM.approved_amount_usdc))
        )
        return float(result.scalar_one() or 0.0)

    async def create(self, loan: AdvanceLoanORM) -> AdvanceLoanORM:
        self.session.add(loan)
        await self.session.commit()
        await self.session.refresh(loan)
        return loan

    async def update(self, loan: AdvanceLoanORM) -> AdvanceLoanORM:
        await self.session.commit()
        await self.session.refresh(loan)
        return loan


class PoolRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_pool(self, pool_id: str) -> Optional[VaquitaPoolORM]:
        result = await self.session.execute(
            select(VaquitaPoolORM).where(VaquitaPoolORM.id == pool_id)
        )
        return result.scalar_one_or_none()

    async def ensure_pool(self, pool_id: str, initial_liquidity: float) -> VaquitaPoolORM:
        pool = await self.get_pool(pool_id)
        if not pool:
            pool = VaquitaPoolORM(
                id=pool_id,
                total_liquidity_usdc=initial_liquidity,
                reserved_liquidity_usdc=0.0,
            )
            self.session.add(pool)
            await self.session.commit()
            await self.session.refresh(pool)
        return pool

    async def reserve_liquidity(self, pool_id: str, amount_usdc: float) -> VaquitaPoolORM:
        pool = await self.get_pool(pool_id)
        if not pool:
            raise EntityNotFoundException("VaquitaPool", pool_id)

        available = pool.total_liquidity_usdc - pool.reserved_liquidity_usdc
        if amount_usdc > available:
            raise InsufficientLiquidityException(requested=amount_usdc, available=available)

        pool.reserved_liquidity_usdc = round(pool.reserved_liquidity_usdc + amount_usdc, 2)
        await self.session.commit()
        await self.session.refresh(pool)
        return pool

    async def release_and_reward(
        self,
        pool_id: str,
        principal_usdc: float,
        yield_usdc: float,
    ) -> VaquitaPoolORM:
        pool = await self.get_pool(pool_id)
        if not pool:
            raise EntityNotFoundException("VaquitaPool", pool_id)

        pool.reserved_liquidity_usdc = max(0.0, round(pool.reserved_liquidity_usdc - principal_usdc, 2))
        pool.total_liquidity_usdc = round(pool.total_liquidity_usdc + yield_usdc, 2)
        await self.session.commit()
        await self.session.refresh(pool)
        return pool
