"""
SimpleKeth — Prediction Service Schemas
Pydantic models for request/response validation matching the API contract.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ─── Request ─────────────────────────────────────────

class PredictionRequest(BaseModel):
    """POST /predict request body."""
    farmer_id: Optional[str] = Field(None, alias="farmerId", description="Optional farmer ID for personalization")
    crop: str = Field(..., description="Crop/commodity name (e.g., 'onion', 'rice')")
    mandi_id: Optional[str] = Field(None, alias="mandiId", description="Specific mandi ID; if omitted, returns top mandis")
    date: Optional[str] = Field(None, description="Target prediction date (ISO format); defaults to tomorrow")
    quantity_kg: Optional[float] = Field(None, alias="quantityKg", description="Quantity in kg")

    model_config = {"populate_by_name": True}


# ─── Response ────────────────────────────────────────

class FeatureExplanation(BaseModel):
    """Per-feature impact on the prediction (SHAP-like)."""
    feature: str
    impact: float


class SinglePrediction(BaseModel):
    """One mandi's price prediction."""
    mandi_id: str = Field(..., alias="mandiId")
    mandi_name: str = Field("", alias="mandiName")
    date: str
    predicted_price: float = Field(..., alias="predictedPrice")
    price_currency: str = Field("INR", alias="priceCurrency")
    confidence: float
    explanation: list[FeatureExplanation] = []

    model_config = {"populate_by_name": True}


class PredictionResponse(BaseModel):
    """POST /predict response body."""
    predictions: list[SinglePrediction]
    model_version: str = Field(..., alias="modelVersion")
    generated_at: str = Field(..., alias="generatedAt")

    model_config = {"populate_by_name": True}
