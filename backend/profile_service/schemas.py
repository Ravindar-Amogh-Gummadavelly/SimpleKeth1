"""
SimpleKeth — Profile Service Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional


class CreateFarmerRequest(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    language: str = "en"  # en | hi | te


class UpdateFarmerRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    language: Optional[str] = None


class FarmerProfileUpdate(BaseModel):
    location_lat: Optional[float] = Field(None, alias="locationLat")
    location_lng: Optional[float] = Field(None, alias="locationLng")
    location_name: Optional[str] = Field(None, alias="locationName")
    primary_crop: Optional[str] = Field(None, alias="primaryCrop")
    secondary_crops: Optional[list[str]] = Field(None, alias="secondaryCrops")
    avg_quantity_kg: Optional[float] = Field(None, alias="avgQuantityKg")
    transport_cost_per_kg: Optional[float] = Field(None, alias="transportCostPerKg")
    storage_cost_per_kg_day: Optional[float] = Field(None, alias="storageCostPerKgDay")
    estimated_loss_pct: Optional[float] = Field(None, alias="estimatedLossPct")
    preferred_mandis: Optional[list[str]] = Field(None, alias="preferredMandis")

    model_config = {"populate_by_name": True}


class FarmerResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: Optional[str] = None
    language: str
    profile: Optional[dict] = None

    model_config = {"populate_by_name": True}
