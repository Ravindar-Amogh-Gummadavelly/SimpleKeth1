"""
SimpleKeth — LSTM Model
Time-series price prediction using PyTorch LSTM.
"""

import numpy as np
import torch
import torch.nn as nn
from pathlib import Path


class LSTMNet(nn.Module):
    """LSTM neural network for time-series forecasting."""

    def __init__(self, input_size: int = 1, hidden_size: int = 64, num_layers: int = 2):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out


class LSTMPredictor:
    """LSTM-based time series predictor with 30-day lookback window."""

    def __init__(self, lookback: int = 30, epochs: int = 50, lr: float = 0.001):
        self.lookback = lookback
        self.epochs = epochs
        self.lr = lr
        self.model = None
        self.scaler_mean = 0.0
        self.scaler_std = 1.0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def _create_sequences(self, data: np.ndarray):
        """Create lookback sequences for LSTM input."""
        X, y = [], []
        for i in range(self.lookback, len(data)):
            X.append(data[i - self.lookback:i])
            y.append(data[i])
        return np.array(X), np.array(y)

    def _normalize(self, data: np.ndarray) -> np.ndarray:
        """Z-score normalization."""
        self.scaler_mean = data.mean()
        self.scaler_std = data.std()
        return (data - self.scaler_mean) / (self.scaler_std + 1e-8)

    def _denormalize(self, data: np.ndarray) -> np.ndarray:
        """Reverse Z-score normalization."""
        return data * self.scaler_std + self.scaler_mean

    def train(self, prices: np.ndarray):
        """Train LSTM model on price time series."""
        normalized = self._normalize(prices)
        X, y = self._create_sequences(normalized)
        
        X_tensor = torch.FloatTensor(X).unsqueeze(-1).to(self.device)
        y_tensor = torch.FloatTensor(y).unsqueeze(-1).to(self.device)

        self.model = LSTMNet(input_size=1).to(self.device)
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)

        self.model.train()
        for epoch in range(self.epochs):
            output = self.model(X_tensor)
            loss = criterion(output, y_tensor)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (epoch + 1) % 10 == 0:
                print(f"  LSTM Epoch [{epoch+1}/{self.epochs}], Loss: {loss.item():.6f}")

        return self

    def predict(self, recent_prices: np.ndarray) -> float:
        """Predict next price from recent lookback window."""
        if self.model is None:
            raise RuntimeError("Model not trained.")

        normalized = (recent_prices - self.scaler_mean) / (self.scaler_std + 1e-8)
        X = torch.FloatTensor(normalized[-self.lookback:]).unsqueeze(0).unsqueeze(-1).to(self.device)

        self.model.eval()
        with torch.no_grad():
            prediction = self.model(X).item()

        return self._denormalize(np.array([prediction]))[0]

    def save(self, path: str = "artifacts/lstm_model.pth"):
        """Save model to disk."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        torch.save({
            "model_state": self.model.state_dict() if self.model else None,
            "scaler_mean": self.scaler_mean,
            "scaler_std": self.scaler_std,
            "lookback": self.lookback,
        }, path)
        print(f"✅ LSTM model saved to {path}")

    def load(self, path: str = "artifacts/lstm_model.pth"):
        """Load model from disk."""
        checkpoint = torch.load(path, map_location=self.device, weights_only=False)
        self.scaler_mean = checkpoint["scaler_mean"]
        self.scaler_std = checkpoint["scaler_std"]
        self.lookback = checkpoint["lookback"]
        self.model = LSTMNet(input_size=1).to(self.device)
        if checkpoint["model_state"]:
            self.model.load_state_dict(checkpoint["model_state"])
        return self
