"""
SimpleKeth — XGBoost Model
Tabular price prediction using gradient boosted trees.
"""

import xgboost as xgb
import numpy as np
import joblib
from pathlib import Path


class XGBoostPredictor:
    """XGBoost regressor for mandi price prediction."""

    def __init__(self):
        self.model = None
        self.params = {
            "objective": "reg:squarederror",
            "max_depth": 6,
            "learning_rate": 0.1,
            "n_estimators": 200,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "min_child_weight": 3,
            "random_state": 42,
        }

    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train XGBoost model."""
        self.model = xgb.XGBRegressor(**self.params)
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_train, y_train)],
            verbose=False,
        )
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate predictions."""
        if self.model is None:
            raise RuntimeError("Model not trained. Call train() first.")
        return self.model.predict(X)

    def get_feature_importance(self) -> dict:
        """Return feature importance scores."""
        if self.model is None:
            return {}
        return dict(zip(
            [f"f{i}" for i in range(len(self.model.feature_importances_))],
            self.model.feature_importances_.tolist(),
        ))

    def save(self, path: str = "artifacts/xgboost_model.joblib"):
        """Save model to disk."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, path)
        print(f"✅ XGBoost model saved to {path}")

    def load(self, path: str = "artifacts/xgboost_model.joblib"):
        """Load model from disk."""
        self.model = joblib.load(path)
        print(f"✅ XGBoost model loaded from {path}")
        return self
