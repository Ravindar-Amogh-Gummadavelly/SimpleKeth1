"""
SimpleKeth — Notification Dispatcher
Twilio (SMS/Voice) and Firebase (Push) integration.

MVP: Both are mocked and log to console. Set real API keys to enable.
"""

import uuid
from datetime import datetime
from typing import Optional
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.config import get_settings
from .schemas import NotifyResponse

settings = get_settings()


class NotificationDispatcher:
    """Dispatches notifications via configured channels."""

    def __init__(self):
        self.is_twilio_real = settings.twilio_account_sid != "mock_sid"
        self.is_firebase_real = settings.firebase_project_id != "simpleketh-dev" or \
                                os.path.exists(settings.firebase_credentials_path)

    async def dispatch(
        self,
        farmer_id: str,
        channel: str,
        message: str,
        payload: Optional[dict] = None,
    ) -> NotifyResponse:
        """Route notification to appropriate channel handler."""
        notification_id = str(uuid.uuid4())

        if channel == "sms":
            return await self._send_sms(notification_id, farmer_id, message)
        elif channel == "voice":
            return await self._send_voice(notification_id, farmer_id, message)
        elif channel == "push":
            return await self._send_push(notification_id, farmer_id, message, payload)
        else:
            return NotifyResponse(
                success=False,
                notification_id=notification_id,
                channel=channel,
                status="failed",
                message=f"Unknown channel: {channel}",
            )

    async def _send_sms(self, notif_id: str, farmer_id: str, message: str) -> NotifyResponse:
        """Send SMS via Twilio (mocked in MVP)."""
        if self.is_twilio_real:
            try:
                from twilio.rest import Client
                client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
                # In production, look up farmer's phone number from DB
                sms = client.messages.create(
                    body=message,
                    from_=settings.twilio_phone_number,
                    to="+911234567890",  # placeholder — resolve from farmer profile
                )
                return NotifyResponse(
                    success=True,
                    notification_id=notif_id,
                    channel="sms",
                    status="sent",
                    message=f"SMS sent via Twilio: {sms.sid}",
                )
            except Exception as e:
                return NotifyResponse(
                    success=False,
                    notification_id=notif_id,
                    channel="sms",
                    status="failed",
                    message=f"Twilio error: {str(e)}",
                )
        else:
            # Mock mode
            print(f"📱 [MOCK SMS] To farmer {farmer_id}: {message}")
            return NotifyResponse(
                success=True,
                notification_id=notif_id,
                channel="sms",
                status="sent",
                message="[MOCK] SMS logged to console",
            )

    async def _send_voice(self, notif_id: str, farmer_id: str, message: str) -> NotifyResponse:
        """Send voice call via Twilio TwiML (mocked in MVP)."""
        if self.is_twilio_real:
            try:
                from twilio.rest import Client
                client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
                twiml = f'<Response><Say language="hi-IN">{message}</Say></Response>'
                call = client.calls.create(
                    twiml=twiml,
                    from_=settings.twilio_phone_number,
                    to="+911234567890",
                )
                return NotifyResponse(
                    success=True,
                    notification_id=notif_id,
                    channel="voice",
                    status="sent",
                    message=f"Voice call initiated: {call.sid}",
                )
            except Exception as e:
                return NotifyResponse(
                    success=False,
                    notification_id=notif_id,
                    channel="voice",
                    status="failed",
                    message=f"Twilio voice error: {str(e)}",
                )
        else:
            print(f"📞 [MOCK VOICE] To farmer {farmer_id}: {message}")
            return NotifyResponse(
                success=True,
                notification_id=notif_id,
                channel="voice",
                status="sent",
                message="[MOCK] Voice call logged to console",
            )

    async def _send_push(
        self, notif_id: str, farmer_id: str, message: str, payload: Optional[dict]
    ) -> NotifyResponse:
        """Send push notification via Firebase (mocked in MVP)."""
        if self.is_firebase_real:
            try:
                import firebase_admin
                from firebase_admin import messaging
                
                if not firebase_admin._apps:
                    firebase_admin.initialize_app()

                fcm_message = messaging.Message(
                    notification=messaging.Notification(
                        title="SimpleKeth Alert",
                        body=message,
                    ),
                    topic=f"farmer_{farmer_id}",
                    data=payload or {},
                )
                response = messaging.send(fcm_message)
                return NotifyResponse(
                    success=True,
                    notification_id=notif_id,
                    channel="push",
                    status="sent",
                    message=f"Push sent: {response}",
                )
            except Exception as e:
                return NotifyResponse(
                    success=False,
                    notification_id=notif_id,
                    channel="push",
                    status="failed",
                    message=f"Firebase error: {str(e)}",
                )
        else:
            print(f"🔔 [MOCK PUSH] To farmer {farmer_id}: {message}")
            return NotifyResponse(
                success=True,
                notification_id=notif_id,
                channel="push",
                status="sent",
                message="[MOCK] Push notification logged to console",
            )
