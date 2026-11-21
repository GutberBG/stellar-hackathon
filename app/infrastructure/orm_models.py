"""SQLAlchemy ORM models separated from domain entities."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base


class ProducerORM(Base):
    __tablename__ = "producers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    community = Column(String(100), nullable=False)
    cooperative = Column(String(150), nullable=False)
    eudr_latitude = Column(Float, nullable=False)
    eudr_longitude = Column(Float, nullable=False)
    eudr_plot_code = Column(String(60), unique=True, nullable=False, index=True)
    phone = Column(String(30), nullable=False)
    compliance_score = Column(Float, default=0.90, nullable=False)
    risk_tier = Column(String(20), default="BAJO", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    deliveries = relationship("HarvestDeliveryORM", back_populates="producer", cascade="all, delete-orphan")
    loans = relationship("AdvanceLoanORM", back_populates="producer", cascade="all, delete-orphan")


class HarvestDeliveryORM(Base):
    __tablename__ = "harvest_deliveries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    delivery_code = Column(String(50), unique=True, index=True, nullable=False)
    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False, index=True)
    cacao_type = Column(String(20), nullable=False)  # BABA | SECO
    gross_weight_kg = Column(Float, nullable=False)
    moisture_percentage = Column(Float, nullable=False)
    net_dry_weight_kg = Column(Float, nullable=False)
    quality_grade = Column(String(10), nullable=False)  # A | B | C
    base_price_per_kg_usdc = Column(Float, nullable=False)
    final_price_per_kg_usdc = Column(Float, nullable=False)
    total_amount_usdc = Column(Float, nullable=False)
    total_amount_bob = Column(Float, nullable=False)
    eudr_coords = Column(String(100), nullable=False)
    payload_hash = Column(String(64), index=True, nullable=False)
    stellar_tx_hash = Column(String(64), nullable=True)
    status = Column(String(30), default="NOTARIZED", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    producer = relationship("ProducerORM", back_populates="deliveries")


class AdvanceLoanORM(Base):
    __tablename__ = "advance_loans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    loan_code = Column(String(50), unique=True, index=True, nullable=False)
    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False, index=True)
    requested_amount_usdc = Column(Float, nullable=False)
    approved_amount_usdc = Column(Float, nullable=False)
    amount_bob = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    vaquita_reservation_id = Column(String(64), nullable=False)
    trustless_escrow_id = Column(String(64), nullable=False)
    pollar_payout_id = Column(String(64), nullable=False)
    pollar_qr_payload = Column(Text, nullable=False)
    status = Column(String(30), default="ACTIVE_ESCROW", nullable=False)  # ACTIVE_ESCROW | SETTLED | REJECTED
    fee_vaquita_usdc = Column(Float, nullable=True)
    fee_ayni_usdc = Column(Float, nullable=True)
    net_disbursed_usdc = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    settled_at = Column(DateTime(timezone=True), nullable=True)

    producer = relationship("ProducerORM", back_populates="loans")


class VaquitaPoolORM(Base):
    __tablename__ = "vaquita_pool"

    id = Column(String(60), primary_key=True)
    total_liquidity_usdc = Column(Float, default=25000.00, nullable=False)
    reserved_liquidity_usdc = Column(Float, default=0.00, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
