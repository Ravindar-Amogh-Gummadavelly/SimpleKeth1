"""
SimpleKeth — Profile Service Routes
CRUD endpoints for farmer profiles.
"""

from fastapi import APIRouter
from .schemas import (
    CreateFarmerRequest,
    UpdateFarmerRequest,
    FarmerProfileUpdate,
    FarmerResponse,
)
from .services import ProfileManager

router = APIRouter()
manager = ProfileManager()


@router.post("/farmers", response_model=FarmerResponse)
async def create_farmer(request: CreateFarmerRequest):
    """Create a new farmer account."""
    return await manager.create_farmer(request)


@router.get("/farmers/{farmer_id}", response_model=FarmerResponse)
async def get_farmer(farmer_id: str):
    """Get farmer by ID."""
    return await manager.get_farmer(farmer_id)


@router.put("/farmers/{farmer_id}", response_model=FarmerResponse)
async def update_farmer(farmer_id: str, request: UpdateFarmerRequest):
    """Update farmer basic info."""
    return await manager.update_farmer(farmer_id, request)


@router.delete("/farmers/{farmer_id}")
async def delete_farmer(farmer_id: str):
    """Delete a farmer account."""
    return await manager.delete_farmer(farmer_id)


@router.put("/farmers/{farmer_id}/profile", response_model=FarmerResponse)
async def update_profile(farmer_id: str, request: FarmerProfileUpdate):
    """Update farmer's detailed profile (crop, location, transport params)."""
    return await manager.update_profile(farmer_id, request)


@router.get("/mandis")
async def list_mandis():
    """List all available mandis for dropdown/search."""
    return await manager.list_mandis()


@router.get("/crops")
async def list_crops():
    """List all supported crops."""
    return await manager.list_crops()
