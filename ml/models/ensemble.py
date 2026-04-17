"""
SimpleKeth — Ensemble Model
Weighted combination of XGBoost, LSTM, and Prophet predictions.
"""

import numpy as np


class EnsemblePredictor:
    """
    Weighted ensemble combining XGBoost (tabular), LSTM (time-series),
    and Prophet (seasonal) predictions.
    """

    def __init__(
        self,
        xgboost_weight: float = 0.45,
        lstm_weight: float = 0.35,
        prophet_weight: float = 0.20,
    ):
        self.weights = {
            "xgboost": xgboost_weight,
            "lstm": lstm_weight,
            "prophet": prophet_weight,
        }

    def predict(
        self,
        xgboost_pred: float | None = None,
        lstm_pred: float | None = None,
        prophet_pred: float | None = None,
    ) -> dict:
        """
        Combine predictions with weighted average.
        Handles missing model predictions gracefully.
        """
        predictions = {}
        if xgboost_pred is not None:
            predictions["xgboost"] = xgboost_pred
        if lstm_pred is not None:
            predictions["lstm"] = lstm_pred
        if prophet_pred is not None:
            predictions["prophet"] = prophet_pred

        if not predictions:
            raise ValueError("At least one model prediction is required")

        # Re-normalize weights for available models
        total_weight = sum(self.weights[k] for k in predictions.keys())
        normalized_weights = {
            k: self.weights[k] / total_weight for k in predictions.keys()
        }

        # Weighted average
        ensemble_pred = sum(
            predictions[k] * normalized_weights[k] for k in predictions.keys()
        )

        # Confidence based on agreement between models
        if len(predictions) >= 2:
            preds = list(predictions.values())
            mean_pred = np.mean(preds)
            std_pred = np.std(preds)
            cv = std_pred / (mean_pred + 1e-8)  # coefficient of variation
            confidence = max(0.5, min(0.95, 1.0 - cv * 2))
        else:
            confidence = 0.65  # single model = lower confidence

        return {
            "predicted_price": round(ensemble_pred, 2),
            "confidence": round(confidence, 2),
            "model_predictions": predictions,
            "weights_used": normalized_weights,
        }
