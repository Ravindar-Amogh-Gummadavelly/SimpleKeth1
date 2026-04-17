"""
SimpleKeth — Prediction Service Cache
Redis caching layer for prediction results.
"""

import json
import redis.asyncio as redis
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.config import get_settings

settings = get_settings()

# Default TTL: 1 hour
CACHE_TTL_SECONDS = 3600


class PredictionCache:
    """Redis-backed cache for prediction results."""

    def __init__(self):
        self._redis: Optional[redis.Redis] = None

    async def _get_redis(self) -> redis.Redis:
        if self._redis is None:
            try:
                self._redis = redis.from_url(
                    settings.redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                )
                await self._redis.ping()
            except Exception as e:
                print(f"⚠️ Redis not available, cache disabled: {e}")
                self._redis = None
        return self._redis

    def _make_key(self, crop: str, mandi_id: Optional[str], date: Optional[str]) -> str:
        """Generate cache key from prediction parameters."""
        parts = ["pred", crop.lower()]
        if mandi_id:
            parts.append(mandi_id)
        if date:
            parts.append(date)
        return ":".join(parts)

    async def get(self, crop: str, mandi_id: Optional[str], date: Optional[str]) -> Optional[dict]:
        """Retrieve cached prediction, returns None on miss or error."""
        r = await self._get_redis()
        if r is None:
            return None
        try:
            key = self._make_key(crop, mandi_id, date)
            cached = await r.get(key)
            if cached:
                return json.loads(cached)
        except Exception as e:
            print(f"⚠️ Cache get error: {e}")
        return None

    async def set(
        self, crop: str, mandi_id: Optional[str], date: Optional[str], data: dict
    ):
        """Store prediction in cache with TTL."""
        r = await self._get_redis()
        if r is None:
            return
        try:
            key = self._make_key(crop, mandi_id, date)
            # Convert Pydantic models to dict if needed
            if hasattr(data, "model_dump"):
                data = data.model_dump(by_alias=True)
            await r.set(key, json.dumps(data, default=str), ex=CACHE_TTL_SECONDS)
        except Exception as e:
            print(f"⚠️ Cache set error: {e}")

    async def invalidate(self, crop: Optional[str] = None):
        """Invalidate cached predictions (e.g., on model retrain)."""
        r = await self._get_redis()
        if r is None:
            return
        try:
            pattern = f"pred:{crop.lower()}:*" if crop else "pred:*"
            keys = []
            async for key in r.scan_iter(match=pattern):
                keys.append(key)
            if keys:
                await r.delete(*keys)
                print(f"🗑️ Invalidated {len(keys)} cached predictions")
        except Exception as e:
            print(f"⚠️ Cache invalidation error: {e}")
