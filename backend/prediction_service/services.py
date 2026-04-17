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
        from shared.config import get_settings
        self.settings = get_settings()

        self.xgb_model = None
        try:
            from xgboost_model import XGBoostPredictor 
            # Needs sys.path injection for ml
            import sys
            import os
            ml_path = os.path.join(os.path.dirname(__file__), '../../ml/models')
            if ml_path not in sys.path:
                sys.path.append(ml_path)
            from xgboost_model import XGBoostPredictor
            self.xgb_model = XGBoostPredictor().load("ml/artifacts/xgboost_model.joblib")
            print("✅ Successfully loaded real XGBoost model into Prediction Engine.")
        except Exception as e:
            print(f"⚠️ Could not load ML model artifacts, falling back to heuristic Engine: {e}")

    async def fetch_weather_data(self, lat: float, lon: float) -> Optional[dict]:
        """Fetch live weather data from OpenWeather. Gracefully degrades if unavailable."""
        if not self.settings.openweather_api_key or self.settings.openweather_api_key == "your_weather_api_key_here":
            return None
            
        import httpx
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.settings.openweather_api_key}&units=metric"
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    return res.json()
        except Exception as e:
            print(f"Weather API Error: {e}")
        return None

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
            prediction = await self._generate_single_prediction(
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

    async def _generate_single_prediction(
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
        heuristic_price = round(
            base_price * seasonal_factor * mandi_factor * trend_factor * (1 + noise), 2
        )

        predicted_price = heuristic_price
        
        # Pull from our trained XGBoost models if available
        if getattr(self, "xgb_model", None) is not None:
            try:
                import numpy as np
                # The pipeline requires 20 columns: day, month, seasonALS, MAs, lags
                # Creating a dummy tensor mapping the feature dimensions (20 features)
                # In full prod, we'd pull these lags from the Posgres timescale DB
                dummy_features = np.zeros((1, 20)) 
                dummy_features[0, 6] = base_price * mandi_factor # price_ma_3
                dummy_features[0, 12] = base_price * mandi_factor * 0.95 # price_lag_1
                
                xgb_pred = float(self.xgb_model.predict(dummy_features)[0])
                # Blend MVP heuristic with the XGBoost regression tensor
                predicted_price = round((heuristic_price + xgb_pred) / 2, 2)
            except Exception as e:
                print(f"XGB inference error: {e}")

        # Confidence decreases with days ahead
        base_confidence = 0.92
        confidence = round(max(0.55, base_confidence - 0.015 * days_ahead + random.gauss(0, 0.03)), 2)

        # Fetch real weather context if available
        weather_impact = 0.0
        # Hardcoding lat/lon for demo mandis
        lat, lon = (28.6139, 77.2090) if "Delhi" in mandi_info["state"] else (19.7515, 75.7139)
        weather_data = await self.fetch_weather_data(lat, lon)
        
        if weather_data and "weather" in weather_data:
            # Simple heuristic: Rain/Thunderstorm might spike prices slightly due to transport disruption
            condition = weather_data["weather"][0]["main"].lower()
            if condition in ["rain", "thunderstorm", "drizzle"]:
                weather_impact = 0.15
            elif condition in ["clear"]:
                weather_impact = -0.05
        else:
            weather_impact = round(random.gauss(0, 0.1), 2)

        # Generate feature explanations
        explanations = self._generate_explanations(
            seasonal_factor, noise, trend_factor, mandi_factor, weather_impact
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
        weather_impact: float = None,
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
        w_imp = weather_impact if weather_impact is not None else round(random.gauss(-0.1, 0.15), 2)
        explanations.append(FeatureExplanation(
            feature="weather_rainfall",
            impact=max(-1.0, min(1.0, w_imp))
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
