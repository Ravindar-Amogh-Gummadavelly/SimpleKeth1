"""
SimpleKeth — Prediction Service Routes
POST /predict — mandi-level price forecasting.
"""

from fastapi import APIRouter, Depends
from .schemas import PredictionRequest, PredictionResponse
from .services import PredictionEngine
from .cache import PredictionCache

router = APIRouter()
prediction_engine = PredictionEngine()
cache = PredictionCache()


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Generate mandi-level crop price predictions for 7–30 days.
    
    Returns predictions with confidence scores and per-feature explanations.
    Results are cached in Redis for performance.
    """
    # Check cache first
    cached = await cache.get(request.crop, request.mandi_id, request.date)
    if cached:
        return cached

    # Generate fresh prediction
    result = await prediction_engine.predict(
        crop=request.crop,
        mandi_id=request.mandi_id,
        target_date=request.date,
        quantity_kg=request.quantity_kg,
        farmer_id=request.farmer_id,
    )

    # Cache the result
    await cache.set(request.crop, request.mandi_id, request.date, result)

    return result
