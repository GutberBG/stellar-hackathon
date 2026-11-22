"""Pure domain entities and value objects."""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    PRODUCTOR = "PRODUCTOR"
    ACOPIADOR = "ACOPIADOR"
    LIQUIDEZ = "LIQUIDEZ"


class CacaoType(str, Enum):
    BABA = "BABA"
    SECO = "SECO"


class QualityGrade(str, Enum):
    A = "A"
    B = "B"
    C = "C"


class RiskLevel(str, Enum):
    BAJO = "BAJO"
    MEDIO = "MEDIO"
    ALTO = "ALTO"


class LoanStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE_ESCROW = "ACTIVE_ESCROW"
    SETTLED = "SETTLED"
    REJECTED = "REJECTED"


class DeliveryStatus(str, Enum):
    PENDING = "PENDING"
    NOTARIZED = "NOTARIZED"


class UserDomain(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    pollar_wallet_address: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None


class ProducerDomain(BaseModel):
    id: int
    user_id: Optional[int] = None
    name: str
    ci_number: Optional[str] = None
    community: str
    cooperative: str
    eudr_latitude: float
    eudr_longitude: float
    eudr_plot_code: str
    parcel_hectares: float = 2.5
    eudr_certified: bool = True
    phone: str
    bank_account_hint: str = "Bisa / Simple QR"
    compliance_score: float = 0.90
    risk_tier: RiskLevel = RiskLevel.BAJO
    hectares: float = 2.0
    tree_age_years: int = 8
    altitude_m: float = 500.0
    created_at: Optional[datetime] = None


class HarvestDeliveryDomain(BaseModel):
    id: Optional[int] = None
    delivery_code: str
    producer_id: int
    cacao_type: CacaoType
    gross_weight_kg: float
    moisture_percentage: float
    net_dry_weight_kg: float
    quality_grade: QualityGrade
    base_price_per_kg_usdc: float
    final_price_per_kg_usdc: float
    total_amount_usdc: float
    total_amount_bob: float
    eudr_coords: str
    payload_hash: str
    stellar_tx_hash: Optional[str] = None
    status: DeliveryStatus = DeliveryStatus.NOTARIZED
    created_at: Optional[datetime] = None


class AdvanceLoanDomain(BaseModel):
    id: Optional[int] = None
    loan_code: str
    producer_id: int
    requested_amount_usdc: float
    approved_amount_usdc: float
    amount_bob: float
    risk_score: float
    risk_level: RiskLevel
    vaquita_reservation_id: str
    trustless_escrow_id: str
    pollar_payout_id: str
    pollar_qr_payload: str
    status: LoanStatus = LoanStatus.ACTIVE_ESCROW
    fee_vaquita_usdc: Optional[float] = None
    fee_ayni_usdc: Optional[float] = None
    net_disbursed_usdc: Optional[float] = None
    created_at: Optional[datetime] = None
    settled_at: Optional[datetime] = None


class PoolStatusDomain(BaseModel):
    pool_id: str
    total_liquidity_usdc: float
    reserved_liquidity_usdc: float
    available_liquidity_usdc: float
    active_loans_count: int = 0
    updated_at: Optional[datetime] = None
