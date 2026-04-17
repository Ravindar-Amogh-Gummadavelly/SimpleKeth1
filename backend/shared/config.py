"""
SimpleKeth — Shared Configuration
Loads environment variables via Pydantic Settings for all backend services.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Central configuration for all SimpleKeth backend services."""

    # --- Database ---
    database_url: str = "postgresql+asyncpg://simpleketh:simpleketh_pass@localhost:5432/simpleketh"
    database_sync_url: str = "postgresql://simpleketh:simpleketh_pass@localhost:5432/simpleketh"

    # --- Redis ---
    redis_url: str = "redis://localhost:6379/0"

    # --- Auth ---
    api_bearer_token: str = "sk-simpleketh-dev-token-2026"

    # --- Weather API ---
    openweather_api_key: str = "your_weather_api_key_here"

    # --- Twilio (mocked for MVP) ---
    twilio_account_sid: str = "mock_sid"
    twilio_auth_token: str = "mock_token"
    twilio_phone_number: str = "+1234567890"

    # --- Firebase (mocked for MVP) ---
    firebase_project_id: str = "simpleketh-dev"
    firebase_credentials_path: str = "./firebase-credentials.json"

    # --- Service URLs ---
    prediction_service_url: str = "http://localhost:8001"
    recommendation_service_url: str = "http://localhost:8002"
    notification_service_url: str = "http://localhost:8003"
    profile_service_url: str = "http://localhost:8004"

    # --- ML ---
    model_artifacts_path: str = "./ml/artifacts"
    active_model_version: str = "ensemble-v1.0"

    # --- App ---
    app_name: str = "SimpleKeth"
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
