"""
SimpleKeth — Recommendation Service Routes
POST /recommend — SELL NOW / HOLD decision engine.
"""

from fastapi import APIRouter
from .schemas import RecommendationRequest, RecommendationResponse
from .services import RecommendationEngine

router = APIRouter()
engine = RecommendationEngine()


@router.post("/recommend", response_model=RecommendationResponse)
async def recommend(request: RecommendationRequest):
    """
    Generate smart sell/hold recommendation with net profit optimization.
    
    Factors in transport, storage, losses, and commission costs across
    multiple mandis to recommend the profit-maximizing decision.
    """
    result = await engine.recommend(
        farmer_profile=request.farmer_profile,
        crop=request.crop,
        quantity_kg=request.quantity_kg,
        prediction_window_days=request.prediction_window_days or 7,
    )
    return result
