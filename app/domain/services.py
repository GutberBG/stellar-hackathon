"""Pure domain services for cacao yield, pricing, hashing, and factoring fees."""
import hashlib
import json
from typing import Tuple, Dict, Any
from app.domain.models import CacaoType, QualityGrade


class DeliveryCalculationService:
    """Handles agronomic calculations for Alto Beni cacao collection receipts."""

    BABA_CONVERSION_FACTOR: float = 0.33
    MOISTURE_THRESHOLD_PCT: float = 7.5

    GRADE_MULTIPLIERS: Dict[QualityGrade, float] = {
        QualityGrade.A: 1.00,
        QualityGrade.B: 0.90,
        QualityGrade.C: 0.75,
    }

    @classmethod
    def calculate_net_dry_weight(
        cls,
        cacao_type: CacaoType,
        gross_weight_kg: float,
        moisture_percentage: float,
    ) -> Tuple[float, float]:
        """
        Calculates net dry weight equivalent in kg and the applied penalty in kg.
        - BABA: 0.33 factor (mucilage/humidity reduction).
        - SECO: If moisture > 7.5%, the excess % is discounted from gross weight.
        """
        if cacao_type == CacaoType.BABA:
            net_weight = round(gross_weight_kg * cls.BABA_CONVERSION_FACTOR, 2)
            penalty_kg = round(gross_weight_kg - net_weight, 2)
            return net_weight, penalty_kg

        # SECO
        if moisture_percentage > cls.MOISTURE_THRESHOLD_PCT:
            excess_pct = moisture_percentage - cls.MOISTURE_THRESHOLD_PCT
            penalty_kg = round(gross_weight_kg * (excess_pct / 100.0), 2)
            net_weight = round(gross_weight_kg - penalty_kg, 2)
            return max(0.0, net_weight), penalty_kg

        return round(gross_weight_kg, 2), 0.0

    @classmethod
    def calculate_price_and_totals(
        cls,
        net_dry_weight_kg: float,
        base_price_usdc: float,
        quality_grade: QualityGrade,
        exchange_rate_bob: float,
    ) -> Tuple[float, float, float]:
        """
        Calculates adjusted price per kg, total USDC, and total Bolivianos (Bs.).
        """
        multiplier = cls.GRADE_MULTIPLIERS.get(quality_grade, 1.0)
        final_price_usdc = round(base_price_usdc * multiplier, 2)
        total_usdc = round(net_dry_weight_kg * final_price_usdc, 2)
        total_bob = round(total_usdc * exchange_rate_bob, 2)
        return final_price_usdc, total_usdc, total_bob

    @classmethod
    def generate_delivery_hash(cls, payload: Dict[str, Any], eudr_coords: str) -> str:
        """
        Generates deterministic SHA-256 hash combining delivery specifications
        and EUDR zero-deforestation parcel coordinates.
        """
        canonical_content = {
            "payload": payload,
            "eudr_coordinates": eudr_coords,
        }
        encoded = json.dumps(canonical_content, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


class SettlementCalculationService:
    """Calculates settlement fees and net disbursements for factoring loans."""

    @classmethod
    def calculate_settlement(
        cls,
        principal_usdc: float,
        vaquita_fee_pct: float = 0.02,
        ayni_fee_pct: float = 0.005,
    ) -> Tuple[float, float, float]:
        """
        Calculates 2.5% fee breakdown (2% Vaquita Pool, 0.5% Ayni Cacao)
        and total settlement amount in USDC.
        """
        fee_vaquita = round(principal_usdc * vaquita_fee_pct, 2)
        fee_ayni = round(principal_usdc * ayni_fee_pct, 2)
        total_settled_usdc = round(principal_usdc + fee_vaquita + fee_ayni, 2)
        return fee_vaquita, fee_ayni, total_settled_usdc
