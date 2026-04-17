"""
SimpleKeth — Prediction Service
Mandi-level price forecasting with Redis caching and SHAP-like explanations.
Port: 8001
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
import os

# Add parent dir for shared imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from shared.config import get_settings
from .routes import router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    print("🔮 Prediction Service starting...")
    yield
    print("🔮 Prediction Service shutting down...")


app = FastAPI(
    title="SimpleKeth — Prediction Service",
    description="Mandi-level crop price prediction with confidence and explanations.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="", tags=["predictions"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "prediction"}
