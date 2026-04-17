"""
SimpleKeth — Training Orchestrator
Loads data, preprocesses, trains all models, saves artifacts with versioning.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from preprocessing.pipeline import load_data, engineer_features, get_feature_columns, split_data
from models.xgboost_model import XGBoostPredictor
from models.lstm_model import LSTMPredictor
from models.prophet_model import ProphetPredictor
from models.ensemble import EnsemblePredictor
import numpy as np


def train_pipeline(csv_path: str = "ml/data/sample_agmarknet.csv"):
    """Full training pipeline for all models."""
    print("=" * 60)
    print("🌾 SimpleKeth — ML Training Pipeline")
    print("=" * 60)

    # 1. Load & preprocess
    print("\n📊 Loading data...")
    raw_data = load_data(csv_path)
    print(f"   Raw: {len(raw_data)} rows")

    features = engineer_features(raw_data)
    print(f"   Features: {len(features)} rows, {len(features.columns)} columns")

    train_df, test_df = split_data(features)
    print(f"   Train: {len(train_df)}, Test: {len(test_df)}")

    feature_cols = get_feature_columns()
    # Filter to available columns
    available_cols = [c for c in feature_cols if c in features.columns]
    print(f"   Using {len(available_cols)} features")

    X_train = train_df[available_cols].values
    y_train = train_df["modal_price"].values
    X_test = test_df[available_cols].values
    y_test = test_df["modal_price"].values

    # 2. Train XGBoost
    print("\n🌳 Training XGBoost...")
    xgb_model = XGBoostPredictor()
    xgb_model.train(X_train, y_train)
    xgb_preds = xgb_model.predict(X_test)
    xgb_mae = np.mean(np.abs(xgb_preds - y_test))
    xgb_mape = np.mean(np.abs((y_test - xgb_preds) / y_test)) * 100
    print(f"   XGBoost MAE: {xgb_mae:.2f}, MAPE: {xgb_mape:.2f}%")
    xgb_model.save("ml/artifacts/xgboost_model.joblib")

    # 3. Train LSTM (per-mandi)
    print("\n🧠 Training LSTM...")
    lstm_model = LSTMPredictor(lookback=14, epochs=30)  # Shorter lookback for small dataset
    all_prices = train_df["modal_price"].values
    if len(all_prices) >= lstm_model.lookback + 10:
        lstm_model.train(all_prices)
        lstm_pred = lstm_model.predict(all_prices[-lstm_model.lookback:])
        print(f"   LSTM next prediction: {lstm_pred:.2f}")
        lstm_model.save("ml/artifacts/lstm_model.pth")
    else:
        print("   ⚠️ Not enough data for LSTM training, skipping")
        lstm_pred = None

    # 4. Train Prophet
    print("\n📈 Training Prophet...")
    prophet_model = ProphetPredictor()
    # Use first mandi's data
    m001_data = raw_data[raw_data["mandi_id"] == "M001"]
    if len(m001_data) >= 30:
        prophet_model.train(m001_data["date"].values, m001_data["modal_price"].values)
        prophet_preds = prophet_model.predict(days_ahead=7)
        if prophet_preds:
            print(f"   Prophet 7-day forecast: {[p['predicted_price'] for p in prophet_preds]}")
        prophet_model.save("ml/artifacts/prophet_model.joblib")
    else:
        print("   ⚠️ Not enough data for Prophet training")

    # 5. Ensemble evaluation
    print("\n🎯 Ensemble Evaluation...")
    ensemble = EnsemblePredictor()
    if lstm_pred is not None:
        result = ensemble.predict(
            xgboost_pred=float(xgb_preds[-1]),
            lstm_pred=float(lstm_pred),
        )
    else:
        result = ensemble.predict(xgboost_pred=float(xgb_preds[-1]))
    print(f"   Ensemble prediction: ₹{result['predicted_price']}")
    print(f"   Confidence: {result['confidence']}")

    # 6. Summary
    print("\n" + "=" * 60)
    print("✅ Training complete!")
    print(f"   XGBoost MAPE: {xgb_mape:.2f}%")
    
    # Directional accuracy
    actual_direction = np.diff(y_test) > 0
    pred_direction = np.diff(xgb_preds) > 0
    dir_accuracy = np.mean(actual_direction == pred_direction) * 100
    print(f"   Directional accuracy: {dir_accuracy:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    train_pipeline()
