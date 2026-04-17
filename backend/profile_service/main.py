"""
SimpleKeth — Profile Service
Farmer profile CRUD with simple token auth.
Port: 8004
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
    print("👤 Profile Service starting...")
    yield
    print("👤 Profile Service shutting down...")


app = FastAPI(
    title="SimpleKeth — Profile Service",
    description="Farmer profile CRUD with personalization parameters.",
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

app.include_router(router, prefix="", tags=["profiles"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "profile"}
