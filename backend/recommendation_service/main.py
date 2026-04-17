"""
SimpleKeth — Recommendation Service
SELL NOW / HOLD decisions with net profit calculation and multi-mandi comparison.
Port: 8002
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.config import get_settings
from .routes import router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("📊 Recommendation Service starting...")
    yield
    print("📊 Recommendation Service shutting down...")


app = FastAPI(
    title="SimpleKeth — Recommendation Service",
    description="Smart sell/hold recommendations with net profit optimization.",
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

app.include_router(router, prefix="", tags=["recommendations"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "recommendation"}
