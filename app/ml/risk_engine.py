"""Machine Learning Risk Engine for predictive cacao factoring and credit score."""
import os
from typing import List, Tuple, Dict, Any
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from app.core.config import settings
from app.domain.models import RiskLevel
from app.ml.synthetic_data import generate_synthetic_cacao_data


class RiskEngine:
    """
    RandomForest-powered Agronomic Credit Risk Engine.
    Evaluates historical smallholder performance combined with real-time microclimate
    (precipitation, humidity) to calculate underwriting risk and maximum approved advance.
    """

    FEATURE_NAMES = [
        "historical_yield_kg",
        "compliance_rate",
        "quality_score",
        "rainfall_mm",
        "humidity_pct",
        "expected_harvest_kg",
    ]

    def __init__(self, model_path: str = settings.ML_MODEL_PATH):
        self.model_path = model_path
        self.model: RandomForestRegressor = self._load_or_train_model()

    def _load_or_train_model(self) -> RandomForestRegressor:
        """Loads cached model or trains a new one from synthetic data."""
        if os.path.exists(self.model_path):
            try:
                model = joblib.load(self.model_path)
                return model
            except Exception:
                pass  # Fall back to training if corrupted

        # Train a new lightweight model
        df = generate_synthetic_cacao_data(n_samples=500, random_state=42)
        X = df[self.FEATURE_NAMES]
        y = df["risk_score"]

        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=8,
            random_state=42,
            n_jobs=1,
        )
        model.fit(X, y)

        try:
            joblib.dump(model, self.model_path)
        except Exception:
            pass

        return model

    def predict(
        self,
        historical_yield_kg: float,
        compliance_rate: float,
        quality_score: float,
        rainfall_mm: float,
        humidity_pct: float,
        expected_harvest_kg: float,
        base_price_usdc: float = settings.BASE_CACAO_PRICE_USDC_PER_KG,
        exchange_rate_bob: float = settings.EXCHANGE_RATE_USDC_BOB,
    ) -> Dict[str, Any]:
        """
        Infers credit risk score (0-100), risk tier, approved advance percentage (15%-60%),
        maximum advance capacity in USDC and BOB, and Spanish explanatory factors.
        """
        features = pd.DataFrame(
            [[
                historical_yield_kg,
                compliance_rate,
                quality_score,
                rainfall_mm,
                humidity_pct,
                expected_harvest_kg,
            ]],
            columns=self.FEATURE_NAMES,
        )

        raw_pred = float(self.model.predict(features)[0])
        risk_score = round(float(np.clip(raw_pred, 5.0, 95.0)), 1)

        # Classify risk level
        if risk_score <= 35.0:
            risk_level = RiskLevel.BAJO
            # Approved percentage: 50% to 60%
            approved_pct = round(60.0 - (risk_score / 35.0) * 10.0, 1)
        elif risk_score <= 65.0:
            risk_level = RiskLevel.MEDIO
            # Approved percentage: 30% to 49%
            approved_pct = round(49.0 - ((risk_score - 35.0) / 30.0) * 19.0, 1)
        else:
            risk_level = RiskLevel.ALTO
            # Approved percentage: 15% to 29%
            approved_pct = round(29.0 - ((risk_score - 65.0) / 30.0) * 14.0, 1)

        # Enforce strict bounds (15% to 60%)
        approved_pct = float(np.clip(approved_pct, 15.0, 60.0))

        # Financial valuations
        estimated_harvest_value_usdc = round(expected_harvest_kg * base_price_usdc, 2)
        max_advance_usdc = round(estimated_harvest_value_usdc * (approved_pct / 100.0), 2)
        max_advance_bob = round(max_advance_usdc * exchange_rate_bob, 2)

        # Agronomic explanation factors in Spanish
        risk_factors = self._generate_risk_factors(
            rainfall_mm=rainfall_mm,
            humidity_pct=humidity_pct,
            compliance_rate=compliance_rate,
            quality_score=quality_score,
            risk_score=risk_score,
        )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "approved_advance_pct": approved_pct,
            "estimated_harvest_value_usdc": estimated_harvest_value_usdc,
            "max_advance_usdc": max_advance_usdc,
            "max_advance_bob": max_advance_bob,
            "risk_factors": risk_factors,
        }

    def _generate_risk_factors(
        self,
        rainfall_mm: float,
        humidity_pct: float,
        compliance_rate: float,
        quality_score: float,
        risk_score: float,
    ) -> List[str]:
        """Generates realistic agronomic diagnostic factors for cooperative credit analysts."""
        factors: List[str] = []

        # Rainfall analysis
        if 140.0 <= rainfall_mm <= 180.0:
            factors.append(
                f"Precipitación óptima ({rainfall_mm} mm): condición ideal para floración y fructificación en Alto Beni."
            )
        elif rainfall_mm < 80.0:
            factors.append(
                f"Alerta de sequía ({rainfall_mm} mm < 80 mm): estrés hídrico severo reduce floración y llenado de granos."
            )
        elif rainfall_mm > 240.0:
            factors.append(
                f"Alerta fitosanitaria crítica ({rainfall_mm} mm > 240 mm): alto riesgo de proliferación de Moniliasis y Escoba de Bruja."
            )
        else:
            factors.append(
                f"Precipitación moderada ({rainfall_mm} mm): fuera del rango óptimo pero manejable con drenaje de parcela."
            )

        # Humidity analysis
        if humidity_pct > 85.0:
            factors.append(
                f"Humedad relativa crítica ({humidity_pct}%): susceptibilidad elevada a Mazorca Negra (Phytophthora)."
            )
        elif humidity_pct < 65.0:
            factors.append(f"Humedad relativa baja ({humidity_pct}%): pérdida de turgencia foliar.")
        else:
            factors.append(f"Humedad relativa en rango favorable ({humidity_pct}%).")

        # Cooperative compliance
        if compliance_rate >= 0.90:
            factors.append(f"Excelente historial de cumplimiento ({int(compliance_rate * 100)}%) con la cooperativa.")
        elif compliance_rate >= 0.70:
            factors.append(f"Cumplimiento regular ({int(compliance_rate * 100)}%) en temporadas previas.")
        else:
            factors.append(f"Productor nuevo o cumplimiento bajo ({int(compliance_rate * 100)}%): cupo crediticio precautorio.")

        # Quality
        if quality_score >= 0.85:
            factors.append(f"Alta calidad histórica ({int(quality_score * 100)}% Grado A de exportación).")
        else:
            factors.append(f"Calidad histórica mixta ({int(quality_score * 100)}% Grado A).")

        return factors
