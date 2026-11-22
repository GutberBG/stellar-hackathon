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
    hectares: float = Field(default=2.0, gt=0, description="Superficie productiva de la parcela (ha)")
    tree_age_years: int = Field(default=8, ge=0, description="Edad promedio de las plantas (años)")
    altitude_m: float = Field(default=500.0, description="Altitud de la parcela (msnm)")


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
    expected_harvest_kg: Optional[float] = Field(
        default=None, 
        gt=0, 
        description="Volumen estimado a cosechar (kg). Opcional: si no se provee, se predice desde biometría ML."
    )
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
    # Biometric features for ML yield prediction (optional - uses producer defaults if not provided)
    tree_height: Optional[float] = Field(default=None, description="Altura del árbol (cm)")
    diameter: Optional[float] = Field(default=None, description="Diámetro del tronco (cm)")
    crown_radius_group: Optional[float] = Field(default=None, description="Radio de copa promedio (cm)")
    leaf_count: Optional[float] = Field(default=None, description="Conteo de hojas")
    cherelle: Optional[float] = Field(default=None, description="Cherelles por árbol")
    flowering_assessment: Optional[float] = Field(default=None, description="Evaluación de floración (0-3)")
    leaf_flush: Optional[float] = Field(default=None, description="Rebrote foliar")
    crown_radius_1: Optional[float] = Field(default=None, description="Radio copa 1 (cm)")
    crown_radius_2: Optional[float] = Field(default=None, description="Radio copa 2 (cm)")
    crown_radius_3: Optional[float] = Field(default=None, description="Radio copa 3 (cm)")
    crown_radius_4: Optional[float] = Field(default=None, description="Radio copa 4 (cm)")
    crown_depth: Optional[float] = Field(default=None, description="Profundidad de copa (m)")
    single_trunk_circumference: Optional[float] = Field(default=None, description="Circunferencia tronco único (cm)")
    n_trees: Optional[int] = Field(default=None, description="Árboles por hectárea")
    variedad: Optional[str] = Field(default=None, description="Variedad de cacao")
    fert_level: Optional[str] = Field(default=None, description="Nivel de fertilización")


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
    # ML predictions for transparency
    predicted_yield_kg_per_ha: Optional[float] = None
    predicted_yield_g_per_tree: Optional[float] = None
    prob_positive_yield: Optional[float] = None
    forecast_price_usdc_per_kg: Optional[float] = None
    price_trend: Optional[str] = None


class FactoringExecuteRequest(BaseModel):
    producer_id: int
    requested_amount_usdc: float = Field(..., gt=0, description="Monto solicitado de factoring en USDC")
    expected_harvest_kg: Optional[float] = Field(
        default=None, 
        gt=0, 
        description="Cosecha comprometida (kg). Opcional: si no se provee, se predice desde biometría ML."
    )
    rainfall_mm: float = Field(default=160.0, ge=0)
    humidity_pct: float = Field(default=78.0, ge=0, le=100)
    # Biometric features for ML yield prediction
    tree_height: Optional[float] = Field(default=None, description="Altura del árbol (cm)")
    diameter: Optional[float] = Field(default=None, description="Diámetro del tronco (cm)")
    crown_radius_group: Optional[float] = Field(default=None, description="Radio de copa promedio (cm)")
    leaf_count: Optional[float] = Field(default=None, description="Conteo de hojas")
    cherelle: Optional[float] = Field(default=None, description="Cherelles por árbol")
    flowering_assessment: Optional[float] = Field(default=None, description="Evaluación de floración (0-3)")
    leaf_flush: Optional[float] = Field(default=None, description="Rebrote foliar")
    crown_radius_1: Optional[float] = Field(default=None, description="Radio copa 1 (cm)")
    crown_radius_2: Optional[float] = Field(default=None, description="Radio copa 2 (cm)")
    crown_radius_3: Optional[float] = Field(default=None, description="Radio copa 3 (cm)")
    crown_radius_4: Optional[float] = Field(default=None, description="Radio copa 4 (cm)")
    crown_depth: Optional[float] = Field(default=None, description="Profundidad de copa (m)")
    single_trunk_circumference: Optional[float] = Field(default=None, description="Circunferencia tronco único (cm)")
    n_trees: Optional[int] = Field(default=None, description="Árboles por hectárea")
    variedad: Optional[str] = Field(default=None, description="Variedad de cacao")
    fert_level: Optional[str] = Field(default=None, description="Nivel de fertilización")


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


# --- ML PRICE & YIELD SCHEMAS ---
class YieldEstimateRequest(BaseModel):
    """Request for yield estimation per zone/parcel."""
    # Biometric features
    tree_height: float = Field(default=170.0, description="Altura del árbol (cm)")
    diameter: float = Field(default=8.0, description="Diámetro del tronco (cm)")
    crown_radius_group: float = Field(default=90.0, description="Radio de copa promedio (cm)")
    leaf_count: float = Field(default=260.0, description="Conteo de hojas")
    cherelle: float = Field(default=0.3, description="Cherelles por árbol")
    flowering_assessment: float = Field(default=1.0, description="Evaluación de floración (0-3)")
    leaf_flush: float = Field(default=1.6, description="Rebrote foliar")
    crown_radius_1: float = Field(default=90.0, description="Radio copa 1 (cm)")
    crown_radius_2: float = Field(default=90.0, description="Radio copa 2 (cm)")
    crown_radius_3: float = Field(default=90.0, description="Radio copa 3 (cm)")
    crown_radius_4: float = Field(default=90.0, description="Radio copa 4 (cm)")
    crown_depth: float = Field(default=4.0, description="Profundidad de copa (m)")
    single_trunk_circumference: float = Field(default=30.0, description="Circunferencia tronco único (cm)")
    n_trees: int = Field(default=1111, description="Árboles por hectárea")
    # Derived features
    crown_area: float = Field(default=254.0, description="Área de copa (cm²)")
    height_diameter_ratio: float = Field(default=21.0, description="Relación altura/diámetro")
    crown_diameter_ratio: float = Field(default=0.08, description="Relación copa/diámetro")
    crown_depth_ratio: float = Field(default=0.02, description="Relación profundidad de copa")
    cherelle_per_tree: float = Field(default=0.0003, description="Cherelles por árbol")
    flowering_per_tree: float = Field(default=0.001, description="Flores por árbol")
    leaf_flush_per_tree: float = Field(default=0.0014, description="Rebrote por árbol")
    cherelle_flowering_ratio: float = Field(default=0.3, description="Relación cherelle/floración")
    crown_area_m2: float = Field(default=2.5, description="Área de copa (m²)")
    density_ratio: float = Field(default=1.0, description="Ratio de densidad")
    # Categorical features
    variedad: str = Field(default="Nacional", description="Variedad de cacao")
    fert_level: str = Field(default="100%", description="Nivel de fertilización")


class YieldEstimateResponse(BaseModel):
    """Response with yield estimate per tree and per hectare."""
    predicted_yield_g_per_tree: float = Field(description="Rendimiento predicho (g/árbol)")
    predicted_yield_kg_per_ha: float = Field(description="Rendimiento predicho (kg/ha)")
    prob_positive_yield: float = Field(description="Probabilidad de rendimiento > 0")
    expected_log_yield: float = Field(description="Log-rendimiento esperado condicional")


class PriceForecastRequest(BaseModel):
    """Request for cacao price forecast."""
    horizon_days: int = Field(default=30, ge=1, le=365, description="Horizonte de predicción (días)")
    current_price_usdc: float = Field(default=4.80, gt=0, description="Precio spot actual USDC/kg")
    include_confidence: bool = Field(default=True, description="Incluir intervalo de confianza")


class PriceForecastResponse(BaseModel):
    """Response with price forecast."""
    forecast_price_usdc_per_kg: float = Field(description="Precio pronosticado USDC/kg")
    horizon_days: int = Field(description="Horizonte de predicción")
    confidence_lower: Optional[float] = Field(default=None, description="Límite inferior IC 95%")
    confidence_upper: Optional[float] = Field(default=None, description="Límite superior IC 95%")
    trend: str = Field(description="Tendencia: bullish/bearish/neutral")


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
