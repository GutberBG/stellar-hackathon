"""Machine Learning Risk Engine for predictive cacao factoring and credit score.
Uses Two-Stage Model (Zero vs Non-Zero + Log-Target Regression) for zero-inflated target.
Integrates with price forecast for expected revenue estimation.
"""
import os
import numpy as np
import pandas as pd
import joblib
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.domain.models import RiskLevel


class RiskEngine:
    """
    Two-Stage Agronomic Credit Risk Engine.
    
    Stage 1 (Classification): Zero vs Non-zero yield (LightGBM)
    Stage 2 (Regression): Log-target regression on positive yields (LightGBM)
    
    Combines: P(y > 0) * exp(E[log(y) | y > 0]) = expected yield in g/tree
    
    Integrates with price forecast for expected revenue per zone.
    """
    
    # Features used by the two-stage model (must match training)
    FEATURE_NAMES = [
        "tree_height", "diameter", "crown_radius_group", "leaf_count", "cherelle",
        "flowering_assessment", "leaf_flush", "crown_radius_1", "crown_radius_2",
        "crown_radius_3", "crown_radius_4", "crown_depth", "single_trunk_circumference",
        "n_trees", "crown_area", "height_diameter_ratio", "crown_diameter_ratio",
        "crown_depth_ratio", "cherelle_per_tree", "flowering_per_tree",
        "leaf_flush_per_tree", "cherelle_flowering_ratio", "crown_area_m2",
        "density_ratio", "variedad", "fert_level"
    ]
    
    def __init__(self, model_path: Optional[str] = None):
        from app.core.config import settings
        self.model_path = model_path or settings.ML_MODEL_PATH
        self.model = self._load_model()
        
    def _load_model(self):
        """Loads cached two-stage model."""
        if os.path.exists(self.model_path):
            try:
                model = joblib.load(self.model_path)
                print(f"Loaded two-stage model from {self.model_path}")
                return model
            except Exception as e:
                print(f"Failed to load model: {e}")
                raise
        raise FileNotFoundError(f"Model not found at {self.model_path}. Please train first.")

    def predict_yield(
        self,
        # Biometric features
        tree_height: float = 170.0,
        diameter: float = 8.0,
        crown_radius_group: float = 90.0,
        leaf_count: float = 260.0,
        cherelle: float = 0.3,
        flowering_assessment: float = 1.0,
        leaf_flush: float = 1.6,
        crown_radius_1: float = 90.0,
        crown_radius_2: float = 90.0,
        crown_radius_3: float = 90.0,
        crown_radius_4: float = 90.0,
        crown_depth: float = 4.0,
        single_trunk_circumference: float = 30.0,
        n_trees: int = 1111,
        # Derived features
        crown_area: float = 254.0,
        height_diameter_ratio: float = 21.0,
        crown_diameter_ratio: float = 0.08,
        crown_depth_ratio: float = 0.02,
        cherelle_per_tree: float = 0.0003,
        flowering_per_tree: float = 0.001,
        leaf_flush_per_tree: float = 0.0014,
        cherelle_flowering_ratio: float = 0.3,
        crown_area_m2: float = 2.5,
        density_ratio: float = 1.0,
        # Categorical features
        variedad: str = "Nacional",
        fert_level: str = "100%",
    ) -> Dict[str, float]:
        """
        Predicts cacao yield using available model.
        
        Returns:
            - yield_g_per_tree: Expected yield in grams per tree
            - yield_kg_per_ha: Expected yield in kg per hectare
            - prob_positive: Probability of positive yield (P(y>0))
        """
        # Build feature DataFrame matching training schema
        X = pd.DataFrame([{
            "tree_height": tree_height,
            "diameter": diameter,
            "crown_radius_group": crown_radius_group,
            "leaf_count": leaf_count,
            "cherelle": cherelle,
            "flowering_assessment": flowering_assessment,
            "leaf_flush": leaf_flush,
            "crown_radius_1": crown_radius_1,
            "crown_radius_2": crown_radius_2,
            "crown_radius_3": crown_radius_3,
            "crown_radius_4": crown_radius_4,
            "crown_depth": crown_depth,
            "single_trunk_circumference": single_trunk_circumference,
            "n_trees": n_trees,
            "crown_area": crown_area,
            "height_diameter_ratio": height_diameter_ratio,
            "crown_diameter_ratio": crown_diameter_ratio,
            "crown_depth_ratio": crown_depth_ratio,
            "cherelle_per_tree": cherelle_per_tree,
            "flowering_per_tree": flowering_per_tree,
            "leaf_flush_per_tree": leaf_flush_per_tree,
            "cherelle_flowering_ratio": cherelle_flowering_ratio,
            "crown_area_m2": crown_area_m2,
            "density_ratio": density_ratio,
            "variedad": variedad,
            "fert_level": fert_level,
        }])
        
        # Check if model has two-stage structure (clf_ and reg_)
        if hasattr(self.model, 'clf_') and hasattr(self.model, 'reg_'):
            # Two-stage model
            proba = self.model.clf_.predict_proba(X)[0, 1]
            expected_yield_g = self.model.reg_.predict(X)[0]
            expected_yield_g_per_tree = proba * expected_yield_g
        else:
            # Single model (e.g., RandomForestRegressor)
            expected_yield_g_per_tree = self.model.predict(X)[0]
            proba = 1.0  # Assume positive yield for single model
        
        # Convert to kg/ha
        expected_yield_kg_per_ha = (expected_yield_g_per_tree * n_trees) / 1000.0
        
        return {
            "yield_g_per_tree": round(float(expected_yield_g_per_tree), 2),
            "yield_kg_per_ha": round(float(expected_yield_kg_per_ha), 2),
            "prob_positive": round(float(proba), 4),
            "conditional_yield_g_per_tree": round(float(expected_yield_g_per_tree), 2),
        }

    def forecast_price(
        self,
        horizon_days: int = 30,
        current_price_usdc: float = 4.80,
    ) -> Dict[str, Any]:
        """
        Forecasts cacao price using mean-reversion model.
        In production, replace with proper time-series model (ARIMA, Prophet, LSTM).
        """
        long_term_mean = 4.80
        current = current_price_usdc
        horizon_years = horizon_days / 365.0
        
        # Mean reversion speed (half-life ~2 years)
        kappa = 0.35
        
        # Expected price reverts toward long-term mean
        expected_price = long_term_mean + (current - long_term_mean) * np.exp(-kappa * horizon_years)
        
        # Volatility scaling
        annual_vol = 0.15
        horizon_vol = annual_vol * np.sqrt(horizon_years)
        
        # Confidence interval (95%)
        z_95 = 1.96
        lower = expected_price * np.exp(-z_95 * horizon_vol)
        upper = expected_price * np.exp(z_95 * horizon_vol)
        
        # Determine trend
        if expected_price > current * 1.02:
            trend = "bullish"
        elif expected_price < current * 0.98:
            trend = "bearish"
        else:
            trend = "neutral"
        
        return {
            "forecast_price_usdc_per_kg": round(float(expected_price), 4),
            "horizon_days": horizon_days,
            "confidence_lower": round(float(lower), 4),
            "confidence_upper": round(float(upper), 4),
            "trend": trend,
        }

    def predict(
        self,
        historical_yield_kg: float,
        compliance_rate: float,
        quality_score: float,
        rainfall_mm: float,
        humidity_pct: float,
        expected_harvest_kg: float = None,  # Now optional - will be predicted from biometrics
        base_price_usdc: float = None,  # Now optional - will use forecast
        exchange_rate_bob: float = settings.EXCHANGE_RATE_USDC_BOB,
        # Biometric features for yield prediction
        tree_height: float = 170.0,
        diameter: float = 8.0,
        crown_radius_group: float = 90.0,
        leaf_count: float = 260.0,
        cherelle: float = 0.3,
        flowering_assessment: float = 1.0,
        leaf_flush: float = 1.6,
        crown_radius_1: float = 90.0,
        crown_radius_2: float = 90.0,
        crown_radius_3: float = 90.0,
        crown_radius_4: float = 90.0,
        crown_depth: float = 4.0,
        single_trunk_circumference: float = 30.0,
        n_trees: int = 1111,
        variedad: str = "Nacional",
        fert_level: str = "100%",
        # Producer parcel info
        hectares: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Infers credit risk score (0-100), risk tier, approved advance percentage (15%-60%),
        maximum advance capacity in USDC and BOB, and Spanish explanatory factors.
        
        Now uses Two-Stage Model for yield prediction + Price Forecast for revenue estimation.
        """
        # 1. Predict yield from biometric features if not provided
        yield_result = self.predict_yield(
            tree_height=tree_height,
            diameter=diameter,
            crown_radius_group=crown_radius_group,
            leaf_count=leaf_count,
            cherelle=cherelle,
            flowering_assessment=flowering_assessment,
            leaf_flush=leaf_flush,
            crown_radius_1=crown_radius_1,
            crown_radius_2=crown_radius_2,
            crown_radius_3=crown_radius_3,
            crown_radius_4=crown_radius_4,
            crown_depth=crown_depth,
            single_trunk_circumference=single_trunk_circumference,
            n_trees=n_trees,
            variedad=variedad,
            fert_level=fert_level,
        )
        
        # Use predicted yield if not provided, else use provided (for backward compat)
        predicted_yield_kg_ha = yield_result["yield_kg_per_ha"]
        if expected_harvest_kg is None:
            # Calculate total expected harvest from parcel size
            expected_harvest_kg = predicted_yield_kg_ha * hectares
        
        # 2. Forecast price if not provided
        if base_price_usdc is None:
            price_result = self.forecast_price(horizon_days=90)  # 3-month horizon
            base_price_usdc = price_result["forecast_price_usdc_per_kg"]
        else:
            price_result = {"forecast_price_usdc_per_kg": base_price_usdc}
        
        # 3. Calculate risk score based on multiple factors
        # Base risk from yield prediction (lower yield = higher risk)
        yield_risk = max(0, min(100, 100 - (predicted_yield_kg_ha / 2000) * 100))
        
        # Climate risk
        climate_risk = 0
        if rainfall_mm < 80 or rainfall_mm > 240:
            climate_risk += 25
        if humidity_pct > 85:
            climate_risk += 15
        elif humidity_pct < 65:
            climate_risk += 10
        
        # Compliance risk
        compliance_risk = (1 - compliance_rate) * 50
        
        # Quality risk
        quality_risk = (1 - quality_score) * 30
        
        # Combined risk score (weighted)
        risk_score = round(
            0.3 * yield_risk + 
            0.2 * climate_risk + 
            0.3 * compliance_risk + 
            0.2 * quality_risk
        , 1)
        risk_score = float(np.clip(risk_score, 5.0, 95.0))

        # Classify risk level
        if risk_score <= 35.0:
            risk_level = RiskLevel.BAJO
            approved_pct = round(60.0 - (risk_score / 35.0) * 10.0, 1)
        elif risk_score <= 65.0:
            risk_level = RiskLevel.MEDIO
            approved_pct = round(49.0 - ((risk_score - 35.0) / 30.0) * 19.0, 1)
        else:
            risk_level = RiskLevel.ALTO
            approved_pct = round(29.0 - ((risk_score - 65.0) / 30.0) * 14.0, 1)

        approved_pct = float(np.clip(approved_pct, 15.0, 60.0))

        # Financial valuations using ML-predicted yield and forecasted price
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
            predicted_yield_kg_ha=predicted_yield_kg_ha,
            forecast_price=base_price_usdc,
        )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "approved_advance_pct": approved_pct,
            "estimated_harvest_value_usdc": estimated_harvest_value_usdc,
            "max_advance_usdc": max_advance_usdc,
            "max_advance_bob": max_advance_bob,
            "risk_factors": risk_factors,
            # ML predictions for transparency
            "predicted_yield_kg_per_ha": predicted_yield_kg_ha,
            "predicted_yield_g_per_tree": yield_result["yield_g_per_tree"],
            "prob_positive_yield": yield_result["prob_positive"],
            "forecast_price_usdc_per_kg": price_result["forecast_price_usdc_per_kg"],
            "price_trend": price_result.get("trend", "neutral"),
            "expected_harvest_kg": round(expected_harvest_kg, 2),
        }

    def _generate_risk_factors(
        self,
        rainfall_mm: float,
        humidity_pct: float,
        compliance_rate: float,
        quality_score: float,
        risk_score: float,
        predicted_yield_kg_ha: float,
        forecast_price: float,
    ) -> List[str]:
        """Generates realistic agronomic diagnostic factors for cooperative credit analysts."""
        factors: List[str] = []

        # Yield prediction
        factors.append(
            f"Rendimiento predicho por ML: {predicted_yield_kg_ha:.0f} kg/ha."
        )

        # Price forecast
        factors.append(
            f"Precio cacao pronosticado: ${forecast_price:.2f} USDC/kg (horizonte 90 días)."
        )

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