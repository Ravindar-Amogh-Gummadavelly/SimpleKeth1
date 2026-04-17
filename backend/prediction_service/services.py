"""
SimpleKeth — Prediction Engine
Core scoring logic: loads ensemble model, generates predictions with confidence
and SHAP-like per-feature explanations.

For MVP, uses a rule-based simulation until ML models are trained.
"""

import random
import math
from datetime import datetime, timedelta
from typing import Optional
from .schemas import PredictionResponse, SinglePrediction, FeatureExplanation


# Sample mandi data (seeded in DB, replicated here for MVP scoring)
SAMPLE_MANDIS = {
    "M001": {"name": "Azadpur Mandi", "state": "Delhi", "base_price": 1200},
    "M002": {"name": "Lasalgaon Mandi", "state": "Maharashtra", "base_price": 1050},
    "M003": {"name": "Pimpalgaon Mandi", "state": "Maharashtra", "base_price": 980},
}

# Crop base prices (₹ per quintal)
CROP_BASE_PRICES = {
    "onion": 1100,
    "rice": 2200,
    "wheat": 2100,
    "tomato": 1500,
    "potato": 800,
}

# Feature importance weights for explanation generation
FEATURE_WEIGHTS = {
    "recent_price_trend": 0.35,
    "seasonal_pattern": 0.20,
    "weather_rainfall": 0.15,
    "market_arrivals": 0.12,
    "historical_average": 0.10,
    "day_of_week": 0.05,
    "supply_demand": 0.03,
}


class PredictionEngine:
    """
    Generates crop price predictions per mandi.
    
    MVP implementation uses rule-based simulation with realistic noise.
    Production will load XGBoost/LSTM/Prophet ensemble from model artifacts.
    """

    def __init__(self):
        self.model_version = "ensemble-v1.0-mvp"

    async def predict(
        self,
        crop: str,
        mandi_id: Optional[str] = None,
        target_date: Optional[str] = None,
        quantity_kg: Optional[float] = None,
        farmer_id: Optional[str] = None,
    ) -> PredictionResponse:
        """Generate predictions for one or all mandis."""
        now = datetime.utcnow()
        
        # Parse target date or default to tomorrow
        if target_date:
            try:
                pred_date = datetime.fromisoformat(target_date.replace("Z", "+00:00"))
            except ValueError:
                pred_date = now + timedelta(days=1)
        else:
            pred_date = now + timedelta(days=1)

        # Determine which mandis to predict for
        if mandi_id and mandi_id in SAMPLE_MANDIS:
            mandis_to_predict = {mandi_id: SAMPLE_MANDIS[mandi_id]}
        else:
            mandis_to_predict = SAMPLE_MANDIS

        # Get crop base price
        base_price = CROP_BASE_PRICES.get(crop.lower(), 1000)

        # Generate predictions
        predictions = []
        for m_id, m_info in mandis_to_predict.items():
            prediction = self._generate_single_prediction(
                m_id, m_info, crop, base_price, pred_date, now
            )
            predictions.append(prediction)

        # Sort by predicted price descending
        predictions.sort(key=lambda p: p.predicted_price, reverse=True)

        return PredictionResponse(
            predictions=predictions,
            model_version=self.model_version,
            generated_at=now.isoformat() + "Z",
        )

    def _generate_single_prediction(
        self,
        mandi_id: str,
        mandi_info: dict,
        crop: str,
        base_price: float,
        pred_date: datetime,
        now: datetime,
    ) -> SinglePrediction:
        """Generate a single mandi prediction with explanations."""
        # Days ahead affects uncertainty
        days_ahead = max(1, (pred_date - now).days)
        
        # Seasonal factor (prices tend to be higher in summer, lower post-harvest)
        month = pred_date.month
        seasonal_factor = 1.0 + 0.1 * math.sin((month - 3) * math.pi / 6)

        # Mandi-specific price adjustment
        mandi_factor = mandi_info["base_price"] / 1100

        # Trend simulation (slight upward bias)
        trend_factor = 1.0 + 0.002 * days_ahead

        # Random noise (increases with days ahead)
        noise = random.gauss(0, 0.03 * math.sqrt(days_ahead))

        # Final predicted price
        predicted_price = round(
            base_price * seasonal_factor * mandi_factor * trend_factor * (1 + noise), 2
        )

        # Confidence decreases with days ahead
        base_confidence = 0.92
        confidence = round(max(0.55, base_confidence - 0.015 * days_ahead + random.gauss(0, 0.03)), 2)

        # Generate feature explanations
        explanations = self._generate_explanations(
            seasonal_factor, noise, trend_factor, mandi_factor
        )

        return SinglePrediction(
            mandi_id=mandi_id,
            mandi_name=mandi_info["name"],
            date=pred_date.strftime("%Y-%m-%d"),
            predicted_price=predicted_price,
            price_currency="INR",
            confidence=confidence,
            explanation=explanations,
        )

    def _generate_explanations(
        self,
        seasonal_factor: float,
        noise: float,
        trend_factor: float,
        mandi_factor: float,
    ) -> list[FeatureExplanation]:
        """Generate SHAP-like feature explanations for the prediction."""
        explanations = []

        # Recent price trend
        trend_impact = round((trend_factor - 1.0) * 10, 2)
        explanations.append(FeatureExplanation(
            feature="recent_price_trend",
            impact=max(-1.0, min(1.0, trend_impact + random.gauss(0, 0.1)))
        ))

        # Seasonal pattern
        seasonal_impact = round((seasonal_factor - 1.0) * 5, 2)
        explanations.append(FeatureExplanation(
            feature="seasonal_pattern",
            impact=max(-1.0, min(1.0, seasonal_impact))
        ))

        # Weather rainfall
        weather_impact = round(random.gauss(-0.1, 0.15), 2)
        explanations.append(FeatureExplanation(
            feature="weather_rainfall",
            impact=max(-1.0, min(1.0, weather_impact))
        ))

        # Market arrivals
        arrivals_impact = round(random.gauss(0.05, 0.1), 2)
        explanations.append(FeatureExplanation(
            feature="market_arrivals",
            impact=max(-1.0, min(1.0, arrivals_impact))
        ))

        # Historical average
        hist_impact = round((mandi_factor - 1.0) * 2, 2)
        explanations.append(FeatureExplanation(
            feature="historical_average",
            impact=max(-1.0, min(1.0, hist_impact))
        ))

        # Sort by absolute impact
        explanations.sort(key=lambda e: abs(e.impact), reverse=True)
        return explanations
