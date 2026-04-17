"""
SimpleKeth — Notification Service
SMS/Voice (Twilio) and Push (Firebase) notification dispatching.
Port: 8003
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
    print("🔔 Notification Service starting...")
    yield
    print("🔔 Notification Service shutting down...")


app = FastAPI(
    title="SimpleKeth — Notification Service",
    description="SMS, voice, and push notification delivery via Twilio & Firebase.",
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

app.include_router(router, prefix="", tags=["notifications"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "notification"}
