"""ML Forecast API endpoints for price and yield prediction."""
import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
import joblib
import numpy as np
import pandas as pd

from app.api.v1.schemas import (
    YieldEstimateRequest,
    YieldEstimateResponse,
    PriceForecastRequest,
    PriceForecastResponse,
)
from app.core.config import settings

router = APIRouter(tags=["ML Forecast"])

# Global model cache
_model_cache = None


def get_two_stage_model():
    """Load the Two-Stage model from disk."""
    global _model_cache
    if _model_cache is None:
        from app.api.v1.dependencies import get_risk_engine
        engine = get_risk_engine()
        if engine.model is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model not trained yet. Please train the model first."
            )
        _model_cache = engine.model
    return _model_cache


@router.post(
    "/yield/estimate",
    response_model=YieldEstimateResponse,
    summary="Estimate cacao yield per tree and per hectare using Two-Stage Model",
)
async def estimate_yield(
    req: YieldEstimateRequest,
    model=Depends(get_two_stage_model),
) -> YieldEstimateResponse:
    """
    Estimates cacao yield using the Two-Stage Model:
    - Stage 1: Classification (Zero vs Non-zero yield probability)
    - Stage 2: Log-target Regression on positive yields
    
    Returns: P(y>0) * exp(E[log(y)|y>0]) = expected yield in g/tree
    Then converts to kg/ha using tree density (n_trees).
    """
    # Build feature DataFrame matching training schema
    feature_dict = {
        "tree_height": req.tree_height,
        "diameter": req.diameter,
        "crown_radius_group": req.crown_radius_group,
        "leaf_count": req.leaf_count,
        "cherelle": req.cherelle,
        "flowering_assessment": req.flowering_assessment,
        "leaf_flush": req.leaf_flush,
        "crown_radius_1": req.crown_radius_1,
        "crown_radius_2": req.crown_radius_2,
        "crown_radius_3": req.crown_radius_3,
        "crown_radius_4": req.crown_radius_4,
        "crown_depth": req.crown_depth,
        "single_trunk_circumference": req.single_trunk_circumference,
        "n_trees": req.n_trees,
        "crown_area": req.crown_area,
        "height_diameter_ratio": req.height_diameter_ratio,
        "crown_diameter_ratio": req.crown_diameter_ratio,
        "crown_depth_ratio": req.crown_depth_ratio,
        "cherelle_per_tree": req.cherelle_per_tree,
        "flowering_per_tree": req.flowering_per_tree,
        "leaf_flush_per_tree": req.leaf_flush_per_tree,
        "cherelle_flowering_ratio": req.cherelle_flowering_ratio,
        "crown_area_m2": req.crown_area_m2,
        "density_ratio": req.density_ratio,
        "variedad": req.variedad,
        "fert_level": req.fert_level,
    }
    
    X = pd.DataFrame([feature_dict])
    
    # Get predictions from Two-Stage Model
    # Stage 1: Probability of positive yield
    proba = model.clf_.predict_proba(X)[0, 1]
    
    # Stage 2: Expected log-yield (conditional on y>0)
    expected_log_yield = np.log1p(model.reg_.predict(X)[0])
    
    # Combined: P(y>0) * E[y|y>0]
    expected_yield_g = proba * np.expm1(expected_log_yield)
    
    # Convert to kg/ha
    n_trees = req.n_trees
    expected_yield_kg_ha = (expected_yield_g * n_trees) / 1000.0
    
    return YieldEstimateResponse(
        predicted_yield_g_per_tree=round(float(expected_yield_g), 2),
        predicted_yield_kg_per_ha=round(float(expected_yield_kg_ha), 2),
        prob_positive_yield=round(float(proba), 4),
        expected_log_yield=round(float(expected_log_yield), 4),
    )


@router.post(
    "/prices/forecast",
    response_model=PriceForecastResponse,
    summary="Forecast cacao price using simple trend model",
)
async def forecast_price(
    req: PriceForecastRequest,
) -> PriceForecastResponse:
    """
    Forecasts cacao price for a given horizon.
    
    Currently uses a simple mean-reversion model with volatility.
    In production, this would use a proper time-series model (ARIMA, Prophet, LSTM)
    trained on historical ICCO/ICCO daily prices + macro factors.
    """
    # Simple mean-reversion model for cacao prices
    # Long-term mean ~4.80 USDC/kg (ICCO 5-year average)
    # Volatility ~15% annualized
    
    long_term_mean = 4.80
    current = req.current_price_usdc
    horizon_years = req.horizon_days / 365.0
    
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
    
    return PriceForecastResponse(
        forecast_price_usdc_per_kg=round(float(expected_price), 4),
        horizon_days=req.horizon_days,
        confidence_lower=round(float(lower), 4) if req.include_confidence else None,
        confidence_upper=round(float(upper), 4) if req.include_confidence else None,
        trend=trend,
    )