"""
SimpleKeth — ML Preprocessing Pipeline
Data cleaning, feature engineering, and train/test split.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_data(csv_path: str = "data/sample_agmarknet.csv") -> pd.DataFrame:
    """Load and clean Agmarknet CSV data."""
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df = df.sort_values(["mandi_id", "date"]).reset_index(drop=True)
    df = df.dropna(subset=["modal_price"])
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Generate ML features from raw price data."""
    features = df.copy()

    # Time features
    features["day_of_week"] = features["date"].dt.dayofweek
    features["day_of_month"] = features["date"].dt.day
    features["month"] = features["date"].dt.month
    features["is_weekend"] = (features["day_of_week"] >= 5).astype(int)

    # Seasonal encoding
    features["season_sin"] = np.sin(2 * np.pi * features["month"] / 12)
    features["season_cos"] = np.cos(2 * np.pi * features["month"] / 12)

    # Rolling statistics (per mandi)
    for window in [3, 7, 14]:
        features[f"price_ma_{window}"] = (
            features.groupby("mandi_id")["modal_price"]
            .transform(lambda x: x.rolling(window, min_periods=1).mean())
        )
        features[f"price_std_{window}"] = (
            features.groupby("mandi_id")["modal_price"]
            .transform(lambda x: x.rolling(window, min_periods=1).std().fillna(0))
        )

    # Lag features
    for lag in [1, 3, 7]:
        features[f"price_lag_{lag}"] = (
            features.groupby("mandi_id")["modal_price"]
            .shift(lag)
        )

    # Price change / momentum
    features["price_change_1d"] = features.groupby("mandi_id")["modal_price"].pct_change()
    features["price_change_7d"] = features.groupby("mandi_id")["modal_price"].pct_change(7)

    # Arrivals features
    if "arrivals_tonnes" in features.columns:
        features["arrivals_ma_7"] = (
            features.groupby("mandi_id")["arrivals_tonnes"]
            .transform(lambda x: x.rolling(7, min_periods=1).mean())
        )

    # Drop rows with NaN from lagging
    features = features.dropna().reset_index(drop=True)

    return features


def get_feature_columns() -> list[str]:
    """Return list of feature column names for model input."""
    return [
        "day_of_week", "day_of_month", "month", "is_weekend",
        "season_sin", "season_cos",
        "price_ma_3", "price_ma_7", "price_ma_14",
        "price_std_3", "price_std_7", "price_std_14",
        "price_lag_1", "price_lag_3", "price_lag_7",
        "price_change_1d", "price_change_7d",
        "arrivals_ma_7",
        "min_price", "max_price",
    ]


def split_data(
    df: pd.DataFrame, test_ratio: float = 0.2
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Temporal split: last N% of data as test set."""
    split_idx = int(len(df) * (1 - test_ratio))
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]
    return train, test


if __name__ == "__main__":
    data = load_data()
    print(f"Raw data: {len(data)} rows")

    features = engineer_features(data)
    print(f"Engineered features: {len(features)} rows, {len(features.columns)} columns")

    train, test = split_data(features)
    print(f"Train: {len(train)} rows, Test: {len(test)} rows")
    print(f"Feature columns: {get_feature_columns()}")
