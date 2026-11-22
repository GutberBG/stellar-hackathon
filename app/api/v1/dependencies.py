"""FastAPI dependency injection providers following Hexagonal Architecture."""
import os
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.infrastructure.database import get_db
from app.infrastructure.repositories import (
    ProducerRepository,
    DeliveryRepository,
    LoanRepository,
    PoolRepository,
    UserRepository,
)
from app.domain.ports.stellar_port import StellarPort
from app.domain.ports.pollar_port import PollarPort
from app.domain.ports.vaquita_port import VaquitaPort
from app.domain.ports.trustless_port import TrustlessPort
from app.infrastructure.adapters.mock_stellar import MockStellarAdapter
from app.infrastructure.adapters.real_stellar import RealStellarAdapter
from app.infrastructure.adapters.mock_pollar import MockPollarAdapter
from app.infrastructure.adapters.mock_vaquita import MockVaquitaAdapter
from app.infrastructure.adapters.mock_trustless import MockTrustlessAdapter
from app.domain.services import DeliveryCalculationService, SettlementCalculationService
from app.ml.risk_engine import RiskEngine

# Singleton instance of the ML Risk Engine
_risk_engine_instance: RiskEngine | None = None


def get_risk_engine() -> RiskEngine:
    global _risk_engine_instance
    if _risk_engine_instance is None:
        _risk_engine_instance = RiskEngine()
    return _risk_engine_instance


# Repositories
def get_producer_repo(db: AsyncSession = Depends(get_db)) -> ProducerRepository:
    return ProducerRepository(db)


def get_delivery_repo(db: AsyncSession = Depends(get_db)) -> DeliveryRepository:
    return DeliveryRepository(db)


def get_loan_repo(db: AsyncSession = Depends(get_db)) -> LoanRepository:
    return LoanRepository(db)


def get_pool_repo(db: AsyncSession = Depends(get_db)) -> PoolRepository:
    return PoolRepository(db)


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


# Hexagonal Adapters (Swappable for real SDKs)
def get_stellar_adapter() -> StellarPort:
    if (
        settings.STELLAR_USE_REAL_NETWORK
        and settings.STELLAR_SECRET_KEY
        and os.getenv("PYTEST_CURRENT_TEST") is None
    ):
        return RealStellarAdapter(
            secret_key=settings.STELLAR_SECRET_KEY,
            horizon_url=settings.STELLAR_HORIZON_URL,
            network=settings.STELLAR_NETWORK,
        )
    return MockStellarAdapter()


def get_pollar_adapter() -> PollarPort:
    # Future swap: return RealPollarAdapter()
    return MockPollarAdapter()


def get_vaquita_adapter(pool_repo: PoolRepository = Depends(get_pool_repo)) -> VaquitaPort:
    # Future swap: return RealVaquitaAdapter()
    return MockVaquitaAdapter(pool_repo)


def get_trustless_adapter() -> TrustlessPort:
    # Future swap: return RealTrustlessAdapter()
    return MockTrustlessAdapter()


# Pure Domain Services
def get_delivery_service() -> type[DeliveryCalculationService]:
    return DeliveryCalculationService


def get_settlement_service() -> type[SettlementCalculationService]:
    return SettlementCalculationService
