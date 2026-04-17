"""
SimpleKeth — Notification Service Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NotifyRequest(BaseModel):
    """POST /notify request body."""
    farmer_id: str = Field(..., alias="farmerId")
    channel: str = Field(..., description="sms | push | voice")
    message: str
    payload: Optional[dict] = None

    model_config = {"populate_by_name": True}


class NotifyResponse(BaseModel):
    """POST /notify response body."""
    success: bool
    notification_id: str = Field(..., alias="notificationId")
    channel: str
    status: str  # "sent" | "queued" | "failed"
    message: str = ""

    model_config = {"populate_by_name": True}
