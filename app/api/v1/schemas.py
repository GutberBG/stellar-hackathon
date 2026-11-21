"""Pydantic v2 schemas for API requests and responses."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.domain.models import CacaoType, QualityGrade, RiskLevel, LoanStatus, DeliveryStatus


# --- PRODUCER SCHEMAS ---
class ProducerBase(BaseModel):
    name: str
    community: str
    cooperative: str
    eudr_latitude: float
    eudr_longitude: float
    eudr_plot_code: str
    phone: str
    compliance_score: float = 0.90
    risk_tier: RiskLevel = RiskLevel.BAJO


class ProducerResponse(ProducerBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProducerDeliveryBrief(BaseModel):
    id: int
    delivery_code: str
    cacao_type: CacaoType
    net_dry_weight_kg: float
    quality_grade: QualityGrade
    total_amount_usdc: float
    total_amount_bob: float
    stellar_tx_hash: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProducerLoanBrief(BaseModel):
    id: int
    loan_code: str
    requested_amount_usdc: float
    approved_amount_usdc: float
    status: LoanStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProducerDetailResponse(ProducerResponse):
    deliveries_count: int = 0
    total_delivered_kg: float = 0.0
    deliveries: List[ProducerDeliveryBrief] = []
    active_loans: List[ProducerLoanBrief] = []


# --- DELIVERY (ACOPIO) SCHEMAS ---
class DeliveryCreateRequest(BaseModel):
    producer_id: int
    cacao_type: CacaoType = Field(..., description="BABA (fresco en baba) o SECO (fermentado y seco)")
    gross_weight_kg: float = Field(..., gt=0, description="Peso bruto ingresado en báscula (kg)")
    moisture_percentage: float = Field(..., ge=0, le=100, description="Porcentaje de humedad medido (%)")
    quality_grade: QualityGrade = Field(..., description="Grado de calidad: A (1.0x), B (0.90x), C (0.75x)")
    base_price_per_kg_usdc: float = Field(
        default=4.80,
        gt=0,
        description="Precio base de referencia por kg seco en USDC",
    )


class DeliveryResponse(BaseModel):
    id: int
    delivery_code: str
    producer_id: int
    producer_name: Optional[str] = None
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
    status: DeliveryStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class DeliveryListResponse(BaseModel):
    total: int
    items: List[DeliveryResponse]


# --- FACTORING SCHEMAS ---
class FactoringSimulateRequest(BaseModel):
    producer_id: int
    expected_harvest_kg: float = Field(..., gt=0, description="Volumen estimado a cosechar (kg)")
    rainfall_mm: float = Field(
        default=160.0,
        ge=0,
        description="Precipitación acumulada o proyectada del mes (mm). Óptimo: 140-180mm.",
    )
    humidity_pct: float = Field(
        default=78.0,
        ge=0,
        le=100,
        description="Humedad relativa promedio (%). Alerta de hongos >85%.",
    )


class FactoringSimulateResponse(BaseModel):
    producer_id: int
    producer_name: str
    community: str
    cooperative: str
    expected_harvest_kg: float
    risk_score: float
    risk_level: RiskLevel
    approved_advance_pct: float
    estimated_harvest_value_usdc: float
    max_advance_usdc: float
    max_advance_bob: float
    risk_factors: List[str]


class FactoringExecuteRequest(BaseModel):
    producer_id: int
    requested_amount_usdc: float = Field(..., gt=0, description="Monto solicitado de factoring en USDC")
    expected_harvest_kg: float = Field(..., gt=0, description="Cosecha comprometida (kg)")
    rainfall_mm: float = Field(default=160.0, ge=0)
    humidity_pct: float = Field(default=78.0, ge=0, le=100)


class FactoringExecuteResponse(BaseModel):
    loan_id: int
    loan_code: str
    producer_id: int
    producer_name: str
    requested_amount_usdc: float
    approved_amount_usdc: float
    amount_bob: float
    risk_score: float
    risk_level: RiskLevel
    status: LoanStatus
    vaquita_reservation_id: str
    trustless_escrow_id: str
    pollar_payout_id: str
    pollar_qr_payload: str
    qr_deep_link: str
    created_at: datetime


class FactoringSettleResponse(BaseModel):
    loan_id: int
    loan_code: str
    status: LoanStatus
    principal_usdc: float
    fee_vaquita_usdc: float
    fee_ayni_usdc: float
    total_settled_usdc: float
    trustless_settlement_tx: str
    settled_at: datetime
    message: str


class LoanSummaryResponse(BaseModel):
    id: int
    loan_code: str
    producer_id: int
    producer_name: Optional[str] = None
    requested_amount_usdc: float
    approved_amount_usdc: float
    amount_bob: float
    risk_level: RiskLevel
    status: LoanStatus
    trustless_escrow_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- DASHBOARD SCHEMAS ---
class PoolStatusResponse(BaseModel):
    pool_id: str
    total_liquidity_usdc: float
    reserved_liquidity_usdc: float
    available_liquidity_usdc: float


class DashboardResponse(BaseModel):
    vaquita_pool: PoolStatusResponse
    total_advanced_usdc: float
    total_advanced_bob: float
    active_loans_count: int
    settled_loans_count: int
    total_deliveries_count: int
    recent_deliveries: List[DeliveryResponse]
    active_loans: List[LoanSummaryResponse]
