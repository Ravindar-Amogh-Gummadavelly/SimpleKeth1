"""
SimpleKeth — Recommendation Service Schemas
Pydantic models matching the canonical API contract.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ─── Request ─────────────────────────────────────────

class FarmerLocation(BaseModel):
    lat: float
    lng: float


class FarmerProfileInput(BaseModel):
    id: Optional[str] = None
    location: FarmerLocation
    transport_cost_per_kg: float = Field(..., alias="transportCostPerKg")
    storage_cost_per_kg_per_day: float = Field(..., alias="storageCostPerKgPerDay")
    estimated_loss_pct: float = Field(..., alias="estimatedLossPct")

    model_config = {"populate_by_name": True}


class RecommendationRequest(BaseModel):
    """POST /recommend request body."""
    farmer_profile: FarmerProfileInput = Field(..., alias="farmerProfile")
    crop: str
    quantity_kg: float = Field(..., alias="quantityKg")
    prediction_window_days: Optional[int] = Field(7, alias="predictionWindowDays")

    model_config = {"populate_by_name": True}


# ─── Response ────────────────────────────────────────

class RecommendedMandi(BaseModel):
    id: str
    name: str
    distance_km: float = Field(..., alias="distanceKm")

    model_config = {"populate_by_name": True}


class AlternativeMandi(BaseModel):
    id: str
    name: str = ""
    expected_net_profit: float = Field(..., alias="expectedNetProfit")
    distance_km: float = Field(0, alias="distanceKm")

    model_config = {"populate_by_name": True}


class RecommendationResponse(BaseModel):
    """POST /recommend response body."""
    decision: str  # "SELL NOW" | "HOLD"
    recommended_mandi: RecommendedMandi = Field(..., alias="recommendedMandi")
    expected_net_profit: float = Field(..., alias="expectedNetProfit")
    alternative_mandis: list[AlternativeMandi] = Field([], alias="alternativeMandis")
    confidence: float
    rationale_text: str = Field(..., alias="rationaleText")
    model_version: str = Field(..., alias="modelVersion")
    generated_at: str = Field(..., alias="generatedAt")

    model_config = {"populate_by_name": True}
