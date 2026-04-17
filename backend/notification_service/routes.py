"""
SimpleKeth — Notification Service Routes
POST /notify — dispatch SMS, voice, or push notifications.
"""

from fastapi import APIRouter
from .schemas import NotifyRequest, NotifyResponse
from .services import NotificationDispatcher

router = APIRouter()
dispatcher = NotificationDispatcher()


@router.post("/notify", response_model=NotifyResponse)
async def notify(request: NotifyRequest):
    """
    Send a notification to a farmer via SMS, push, or voice call.
    
    For MVP: Twilio and Firebase are mocked. Actual integration requires
    setting real API keys in the environment.
    """
    result = await dispatcher.dispatch(
        farmer_id=request.farmer_id,
        channel=request.channel,
        message=request.message,
        payload=request.payload,
    )
    return result
