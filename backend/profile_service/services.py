"""
SimpleKeth — Profile Manager
In-memory CRUD for MVP. Production will use PostgreSQL via SQLAlchemy.
"""

import uuid
from typing import Optional
from fastapi import HTTPException
from .schemas import (
    CreateFarmerRequest,
    UpdateFarmerRequest,
    FarmerProfileUpdate,
    FarmerResponse,
)


# In-memory store for MVP (replace with DB in production)
_farmers_db: dict[str, dict] = {}


# Mandi reference data (same as recommendation service)
MANDIS = [
    {"id": "M001", "code": "M001", "name": "Azadpur Mandi", "state": "Delhi", "district": "North Delhi",
     "latitude": 28.717, "longitude": 77.177},
    {"id": "M002", "code": "M002", "name": "Lasalgaon Mandi", "state": "Maharashtra", "district": "Nashik",
     "latitude": 20.148, "longitude": 74.230},
    {"id": "M003", "code": "M003", "name": "Pimpalgaon Mandi", "state": "Maharashtra", "district": "Nashik",
     "latitude": 20.273, "longitude": 74.034},
]

CROPS = [
    {"name": "onion", "category": "VEGETABLE", "nameHi": "प्याज", "nameTe": "ఉల్లిపాయ"},
    {"name": "rice", "category": "GRAIN", "nameHi": "चावल", "nameTe": "బియ్యం"},
    {"name": "wheat", "category": "GRAIN", "nameHi": "गेहूं", "nameTe": "గోధుమ"},
    {"name": "tomato", "category": "VEGETABLE", "nameHi": "टमाटर", "nameTe": "టమాటా"},
    {"name": "potato", "category": "VEGETABLE", "nameHi": "आलू", "nameTe": "బంగాళాదుంప"},
]


class ProfileManager:
    """Manages farmer profiles (in-memory for MVP)."""

    async def create_farmer(self, request: CreateFarmerRequest) -> FarmerResponse:
        farmer_id = str(uuid.uuid4())
        farmer = {
            "id": farmer_id,
            "name": request.name,
            "phone": request.phone,
            "email": request.email,
            "language": request.language,
            "profile": None,
        }
        _farmers_db[farmer_id] = farmer
        return FarmerResponse(**farmer)

    async def get_farmer(self, farmer_id: str) -> FarmerResponse:
        if farmer_id not in _farmers_db:
            raise HTTPException(status_code=404, detail="Farmer not found")
        return FarmerResponse(**_farmers_db[farmer_id])

    async def update_farmer(
        self, farmer_id: str, request: UpdateFarmerRequest
    ) -> FarmerResponse:
        if farmer_id not in _farmers_db:
            raise HTTPException(status_code=404, detail="Farmer not found")
        farmer = _farmers_db[farmer_id]
        if request.name is not None:
            farmer["name"] = request.name
        if request.email is not None:
            farmer["email"] = request.email
        if request.language is not None:
            farmer["language"] = request.language
        return FarmerResponse(**farmer)

    async def delete_farmer(self, farmer_id: str) -> dict:
        if farmer_id not in _farmers_db:
            raise HTTPException(status_code=404, detail="Farmer not found")
        del _farmers_db[farmer_id]
        return {"deleted": True, "id": farmer_id}

    async def update_profile(
        self, farmer_id: str, request: FarmerProfileUpdate
    ) -> FarmerResponse:
        if farmer_id not in _farmers_db:
            raise HTTPException(status_code=404, detail="Farmer not found")
        farmer = _farmers_db[farmer_id]
        profile_data = request.model_dump(exclude_none=True, by_alias=False)
        if farmer["profile"] is None:
            farmer["profile"] = profile_data
        else:
            farmer["profile"].update(profile_data)
        return FarmerResponse(**farmer)

    async def list_mandis(self) -> list[dict]:
        return MANDIS

    async def list_crops(self) -> list[dict]:
        return CROPS
