"""
SimpleKeth — Prophet Model
Seasonal decomposition and trend forecasting.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import joblib


class ProphetPredictor:
    """Facebook Prophet model for seasonal price forecasting."""

    def __init__(self):
        self.model = None

    def train(self, dates: np.ndarray, prices: np.ndarray):
        """Train Prophet model."""
        try:
            from prophet import Prophet

            df = pd.DataFrame({
                "ds": pd.to_datetime(dates),
                "y": prices,
            })

            self.model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                changepoint_prior_scale=0.05,
            )
            self.model.fit(df)
            print("✅ Prophet model trained")
        except ImportError:
            print("⚠️ Prophet not installed, using fallback")
            self.model = None
        return self

    def predict(self, days_ahead: int = 7) -> list[dict]:
        """Predict future prices."""
        if self.model is None:
            return []

        future = self.model.make_future_dataframe(periods=days_ahead)
        forecast = self.model.predict(future)

        predictions = []
        for _, row in forecast.tail(days_ahead).iterrows():
            predictions.append({
                "date": row["ds"].isoformat(),
                "predicted_price": round(row["yhat"], 2),
                "lower_bound": round(row["yhat_lower"], 2),
                "upper_bound": round(row["yhat_upper"], 2),
            })
        return predictions

    def save(self, path: str = "artifacts/prophet_model.joblib"):
        """Save model to disk."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, path)
        print(f"✅ Prophet model saved to {path}")

    def load(self, path: str = "artifacts/prophet_model.joblib"):
        """Load model from disk."""
        self.model = joblib.load(path)
        return self
