"""
SimpleKeth — Profile Service Tests
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from profile_service.main import app

client = TestClient(app)


class TestHealthCheck:
    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200


class TestFarmerCRUD:
    def test_create_farmer(self):
        """POST /farmers should create a farmer and return ID."""
        response = client.post("/farmers", json={
            "name": "Ramesh Kumar",
            "phone": "+919876543210",
            "language": "hi"
        })
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "Ramesh Kumar"
        assert data["language"] == "hi"

    def test_get_farmer(self):
        """GET /farmers/{id} should return farmer details."""
        # Create first
        create_resp = client.post("/farmers", json={
            "name": "Test Farmer",
            "phone": "+919999999999"
        })
        farmer_id = create_resp.json()["id"]

        # Get
        response = client.get(f"/farmers/{farmer_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Test Farmer"

    def test_update_farmer(self):
        """PUT /farmers/{id} should update farmer info."""
        create_resp = client.post("/farmers", json={
            "name": "Before Update",
            "phone": "+918888888888"
        })
        farmer_id = create_resp.json()["id"]

        response = client.put(f"/farmers/{farmer_id}", json={
            "name": "After Update",
            "language": "te"
        })
        assert response.status_code == 200
        assert response.json()["name"] == "After Update"
        assert response.json()["language"] == "te"

    def test_delete_farmer(self):
        """DELETE /farmers/{id} should remove the farmer."""
        create_resp = client.post("/farmers", json={
            "name": "To Delete",
            "phone": "+917777777777"
        })
        farmer_id = create_resp.json()["id"]

        response = client.delete(f"/farmers/{farmer_id}")
        assert response.status_code == 200

        # Verify deleted
        get_resp = client.get(f"/farmers/{farmer_id}")
        assert get_resp.status_code == 404

    def test_update_profile(self):
        """PUT /farmers/{id}/profile should update crop and location params."""
        create_resp = client.post("/farmers", json={
            "name": "Profile Test",
            "phone": "+916666666666"
        })
        farmer_id = create_resp.json()["id"]

        response = client.put(f"/farmers/{farmer_id}/profile", json={
            "primaryCrop": "onion",
            "avgQuantityKg": 750,
            "transportCostPerKg": 2.0,
            "estimatedLossPct": 3
        })
        assert response.status_code == 200
        profile = response.json()["profile"]
        assert profile["primary_crop"] == "onion"
        assert profile["avg_quantity_kg"] == 750


class TestReferenceData:
    def test_list_mandis(self):
        """GET /mandis should return mandi list."""
        response = client.get("/mandis")
        assert response.status_code == 200
        mandis = response.json()
        assert len(mandis) == 3
        assert mandis[0]["name"] == "Azadpur Mandi"

    def test_list_crops(self):
        """GET /crops should return crop list with translations."""
        response = client.get("/crops")
        assert response.status_code == 200
        crops = response.json()
        assert len(crops) >= 5
        onion = next(c for c in crops if c["name"] == "onion")
        assert onion["nameHi"] == "प्याज"
        assert onion["nameTe"] == "ఉల్లిపాయ"
