"""
SimpleKeth — Notification Service Tests
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from notification_service.main import app

client = TestClient(app)


class TestHealthCheck:
    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["service"] == "notification"


class TestNotifyEndpoint:
    def test_sms_notification_mock(self):
        """POST /notify with SMS channel should succeed (mocked)."""
        response = client.post("/notify", json={
            "farmerId": "test-farmer-1",
            "channel": "sms",
            "message": "Onion price spike! Sell now at Azadpur Mandi."
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["channel"] == "sms"
        assert data["status"] == "sent"

    def test_voice_notification_mock(self):
        """POST /notify with voice channel should succeed (mocked)."""
        response = client.post("/notify", json={
            "farmerId": "test-farmer-1",
            "channel": "voice",
            "message": "प्याज की कीमत बढ़ गई है।"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["channel"] == "voice"

    def test_push_notification_mock(self):
        """POST /notify with push channel should succeed (mocked)."""
        response = client.post("/notify", json={
            "farmerId": "test-farmer-1",
            "channel": "push",
            "message": "Price alert!",
            "payload": {"crop": "onion", "price": 1350}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_unknown_channel_fails(self):
        """POST /notify with unknown channel should return failure."""
        response = client.post("/notify", json={
            "farmerId": "test-farmer-1",
            "channel": "telegram",
            "message": "test"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert data["status"] == "failed"

    def test_notification_returns_id(self):
        """Response should include a unique notification ID."""
        response = client.post("/notify", json={
            "farmerId": "test-farmer-1",
            "channel": "sms",
            "message": "test alert"
        })
        data = response.json()
        assert "notificationId" in data
        assert len(data["notificationId"]) > 10
