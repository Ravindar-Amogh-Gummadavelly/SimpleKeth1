"""
SimpleKeth — Prediction Service Tests
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from prediction_service.main import app

client = TestClient(app)


class TestHealthCheck:
    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert response.json()["service"] == "prediction"


class TestPredictEndpoint:
    def test_predict_with_crop_only(self):
        """POST /predict with just crop should return predictions for all mandis."""
        response = client.post("/predict", json={"crop": "onion"})
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert "modelVersion" in data
        assert "generatedAt" in data
        assert len(data["predictions"]) >= 1

    def test_predict_with_specific_mandi(self):
        """POST /predict with mandiId should return prediction for that mandi."""
        response = client.post("/predict", json={
            "crop": "onion",
            "mandiId": "M001",
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data["predictions"]) == 1
        assert data["predictions"][0]["mandiId"] == "M001"

    def test_prediction_has_required_fields(self):
        """Each prediction should have all required fields from API contract."""
        response = client.post("/predict", json={"crop": "onion"})
        data = response.json()
        pred = data["predictions"][0]

        assert "mandiId" in pred
        assert "date" in pred
        assert "predictedPrice" in pred
        assert "confidence" in pred
        assert "explanation" in pred
        assert pred["priceCurrency"] == "INR"

    def test_prediction_has_explanations(self):
        """Each prediction should include per-feature explanations."""
        response = client.post("/predict", json={"crop": "rice"})
        data = response.json()
        pred = data["predictions"][0]

        assert len(pred["explanation"]) >= 1
        exp = pred["explanation"][0]
        assert "feature" in exp
        assert "impact" in exp

    def test_confidence_in_valid_range(self):
        """Confidence should be between 0 and 1."""
        response = client.post("/predict", json={"crop": "wheat"})
        data = response.json()
        for pred in data["predictions"]:
            assert 0 <= pred["confidence"] <= 1

    def test_model_version_present(self):
        """Response should include model version."""
        response = client.post("/predict", json={"crop": "onion"})
        data = response.json()
        assert data["modelVersion"].startswith("ensemble")

    def test_unknown_crop_returns_predictions(self):
        """Unknown crop should still return predictions (with default base price)."""
        response = client.post("/predict", json={"crop": "soybean"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["predictions"]) >= 1
