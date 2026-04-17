"""
SimpleKeth — Recommendation Service Tests
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from recommendation_service.main import app

client = TestClient(app)


class TestHealthCheck:
    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["service"] == "recommendation"


class TestRecommendEndpoint:
    VALID_REQUEST = {
        "farmerProfile": {
            "location": {"lat": 28.61, "lng": 77.20},
            "transportCostPerKg": 1.5,
            "storageCostPerKgPerDay": 0.5,
            "estimatedLossPct": 5
        },
        "crop": "onion",
        "quantityKg": 500,
        "predictionWindowDays": 7
    }

    def test_recommend_returns_decision(self):
        """POST /recommend should return SELL NOW or HOLD."""
        response = client.post("/recommend", json=self.VALID_REQUEST)
        assert response.status_code == 200
        data = response.json()
        assert data["decision"] in ["SELL NOW", "HOLD"]

    def test_recommend_has_mandi(self):
        """Response should include recommended mandi with name and distance."""
        response = client.post("/recommend", json=self.VALID_REQUEST)
        data = response.json()
        mandi = data["recommendedMandi"]
        assert "id" in mandi
        assert "name" in mandi
        assert "distanceKm" in mandi
        assert mandi["distanceKm"] > 0

    def test_recommend_has_profit(self):
        """Response should include expected net profit."""
        response = client.post("/recommend", json=self.VALID_REQUEST)
        data = response.json()
        assert "expectedNetProfit" in data
        assert isinstance(data["expectedNetProfit"], (int, float))

    def test_recommend_has_alternatives(self):
        """Response should include alternative mandis."""
        response = client.post("/recommend", json=self.VALID_REQUEST)
        data = response.json()
        assert "alternativeMandis" in data
        assert len(data["alternativeMandis"]) >= 1
        alt = data["alternativeMandis"][0]
        assert "id" in alt
        assert "expectedNetProfit" in alt

    def test_recommend_has_confidence(self):
        """Response should include confidence score."""
        response = client.post("/recommend", json=self.VALID_REQUEST)
        data = response.json()
        assert 0 <= data["confidence"] <= 1

    def test_recommend_has_rationale(self):
        """Response should include human-readable rationale."""
        response = client.post("/recommend", json=self.VALID_REQUEST)
        data = response.json()
        assert len(data["rationaleText"]) > 20

    def test_recommend_has_model_version(self):
        """Response should include model version and timestamp."""
        response = client.post("/recommend", json=self.VALID_REQUEST)
        data = response.json()
        assert "modelVersion" in data
        assert "generatedAt" in data
