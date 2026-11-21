"""Synthetic agronomic and credit dataset generator for Alto Beni & Palos Blancos cacao smallholders."""
import numpy as np
import pandas as pd


def generate_synthetic_cacao_data(n_samples: int = 500, random_state: int = 42) -> pd.DataFrame:
    """
    Generates a realistic agronomic dataset (500 records) tailored to the tropical
    foothills of North La Paz, Bolivia (Alto Beni, Sapecho, Palos Blancos).

    Variables:
    - historical_yield_kg: Average dry cacao harvested in previous seasons (kg).
    - compliance_rate: Ratio of contracted volume actually delivered (0.50 to 1.0).
    - quality_score: Historical % of Grade A export cacao (0.50 to 1.0).
    - rainfall_mm: Projected or observed monthly rainfall during pod development (50 to 320 mm).
    - humidity_pct: Relative humidity (55% to 98%).
    - expected_harvest_kg: Farmer's self-reported or agronomist-estimated volume.
    - risk_score: Target continuous variable (0 - 100), where lower is safer.
    """
    np.random.seed(random_state)

    # 1. Historical harvest volumes (log-normal distribution typical for smallholders with 1-4 hectares)
    historical_yield_kg = np.clip(np.random.normal(loc=950, scale=350, size=n_samples), 250, 2400)

    # 2. Historical cooperative compliance rate
    compliance_rate = np.clip(np.random.beta(a=7, b=2, size=n_samples), 0.50, 1.0)

    # 3. Quality score (% Grade A)
    quality_score = np.clip(np.random.beta(a=6, b=2.5, size=n_samples), 0.50, 1.0)

    # 4. Climatic variables for Alto Beni (wet tropical valley)
    # Optimal rainfall is 140 - 180 mm.
    # Below 80 mm represents drought. Above 240 mm represents moniliasis risk.
    rainfall_mm = np.clip(np.random.normal(loc=170, scale=60, size=n_samples), 45, 330)
    humidity_pct = np.clip(np.random.normal(loc=78, scale=10, size=n_samples), 55, 98)

    # 5. Expected harvest volume for current season
    expected_harvest_kg = np.clip(
        historical_yield_kg * np.random.uniform(0.85, 1.15, size=n_samples),
        200,
        2500,
    )

    # 6. Agronomic Risk Calculation (Ground Truth with Noise)
    # Base risk from credit & quality profile:
    base_risk = (1.0 - compliance_rate) * 45.0 + (1.0 - quality_score) * 25.0

    # Climate penalty:
    climate_penalty = np.zeros(n_samples)
    for i in range(n_samples):
        r = rainfall_mm[i]
        h = humidity_pct[i]

        # Drought penalty
        if r < 80.0:
            climate_penalty[i] += 28.0 + (80.0 - r) * 0.35
        # Optimal rain bonus
        elif 140.0 <= r <= 180.0:
            climate_penalty[i] -= 12.0
        # Excessive rain + high humidity = Moniliasis fungal outbreak
        elif r > 240.0:
            climate_penalty[i] += 22.0 + (r - 240.0) * 0.25
            if h > 85.0:
                climate_penalty[i] += 12.0

        # High humidity baseline penalty
        if h > 88.0 and r > 180.0:
            climate_penalty[i] += 8.0

    # Combine with realistic stochastic error
    noise = np.random.normal(loc=0.0, scale=4.0, size=n_samples)
    raw_risk = 25.0 + base_risk + climate_penalty + noise

    # Strict normalization between 5.0 and 95.0
    risk_score = np.clip(raw_risk, 5.0, 95.0)

    df = pd.DataFrame(
        {
            "historical_yield_kg": np.round(historical_yield_kg, 2),
            "compliance_rate": np.round(compliance_rate, 4),
            "quality_score": np.round(quality_score, 4),
            "rainfall_mm": np.round(rainfall_mm, 1),
            "humidity_pct": np.round(humidity_pct, 1),
            "expected_harvest_kg": np.round(expected_harvest_kg, 2),
            "risk_score": np.round(risk_score, 2),
        }
    )

    return df
