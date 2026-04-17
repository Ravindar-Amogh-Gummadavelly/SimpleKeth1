"""
SimpleKeth — Shared SQLAlchemy ORM Models
Mirrors the Prisma schema for use in FastAPI services.
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    String, Float, Boolean, DateTime, Text, JSON,
    ForeignKey, Index, UniqueConstraint, Enum as SAEnum,
    ARRAY,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import enum


# ─── Enums ──────────────────────────────────────────

class DecisionType(str, enum.Enum):
    SELL_NOW = "SELL_NOW"
    HOLD = "HOLD"


class NotificationChannel(str, enum.Enum):
    SMS = "SMS"
    PUSH = "PUSH"
    VOICE = "VOICE"


class NotificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"


# ─── Farmer ─────────────────────────────────────────

class Farmer(Base):
    __tablename__ = "farmers"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(5), default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    profile = relationship("FarmerProfile", back_populates="farmer", uselist=False, cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="farmer")
    notifications = relationship("Notification", back_populates="farmer", cascade="all, delete-orphan")


class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    farmer_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("farmers.id", ondelete="CASCADE"), unique=True
    )
    location_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    location_lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    location_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    primary_crop: Mapped[str | None] = mapped_column(String(100), nullable=True)
    secondary_crops: Mapped[list | None] = mapped_column(ARRAY(String), nullable=True, default=[])
    avg_quantity_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    transport_cost_per_kg: Mapped[float] = mapped_column(Float, default=1.5)
    storage_cost_per_kg_day: Mapped[float] = mapped_column(Float, default=0.5)
    estimated_loss_pct: Mapped[float] = mapped_column(Float, default=5.0)
    preferred_mandis: Mapped[list | None] = mapped_column(ARRAY(String), nullable=True, default=[])
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    farmer = relationship("Farmer", back_populates="profile")


# ─── Mandi ──────────────────────────────────────────

class Mandi(Base):
    __tablename__ = "mandis"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    code: Mapped[str] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    state: Mapped[str] = mapped_column(String(100))
    district: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    commission_pct: Mapped[float] = mapped_column(Float, default=2.5)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    prices = relationship("MandiPrice", back_populates="mandi", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="mandi", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="mandi")
    transport_rates = relationship("TransportRate", back_populates="mandi", cascade="all, delete-orphan")


# ─── MandiPrice ─────────────────────────────────────

class MandiPrice(Base):
    __tablename__ = "mandi_prices"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    mandi_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("mandis.id", ondelete="CASCADE")
    )
    commodity: Mapped[str] = mapped_column(String(100))
    variety: Mapped[str | None] = mapped_column(String(100), nullable=True)
    min_price: Mapped[float] = mapped_column(Float)
    max_price: Mapped[float] = mapped_column(Float)
    modal_price: Mapped[float] = mapped_column(Float)
    arrivals_tonnes: Mapped[float | None] = mapped_column(Float, nullable=True)
    price_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    mandi = relationship("Mandi", back_populates="prices")

    __table_args__ = (
        UniqueConstraint("mandi_id", "commodity", "price_date", name="uq_mandi_commodity_date"),
        Index("ix_mandi_commodity_date", "mandi_id", "commodity", "price_date"),
        Index("ix_commodity_date", "commodity", "price_date"),
    )


# ─── Prediction ─────────────────────────────────────

class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    mandi_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("mandis.id", ondelete="CASCADE")
    )
    commodity: Mapped[str] = mapped_column(String(100))
    predicted_price: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)
    prediction_date: Mapped[datetime] = mapped_column(DateTime)
    explanation: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    model_version: Mapped[str] = mapped_column(String(50))
    generated_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    mandi = relationship("Mandi", back_populates="predictions")

    __table_args__ = (
        Index("ix_pred_mandi_commodity_date", "mandi_id", "commodity", "prediction_date"),
    )


# ─── Recommendation ─────────────────────────────────

class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    farmer_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("farmers.id"), nullable=True
    )
    mandi_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("mandis.id")
    )
    commodity: Mapped[str] = mapped_column(String(100))
    quantity_kg: Mapped[float] = mapped_column(Float)
    decision: Mapped[DecisionType] = mapped_column(SAEnum(DecisionType))
    expected_net_profit: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)
    rationale_text: Mapped[str] = mapped_column(Text)
    alternative_mandis: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    model_version: Mapped[str] = mapped_column(String(50))
    generated_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    farmer = relationship("Farmer", back_populates="recommendations")
    mandi = relationship("Mandi", back_populates="recommendations")

    __table_args__ = (
        Index("ix_rec_farmer_commodity", "farmer_id", "commodity", "generated_at"),
    )


# ─── TransportRate ──────────────────────────────────

class TransportRate(Base):
    __tablename__ = "transport_rates"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    mandi_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("mandis.id", ondelete="CASCADE")
    )
    from_location_name: Mapped[str] = mapped_column(String(255))
    distance_km: Mapped[float] = mapped_column(Float)
    cost_per_kg: Mapped[float] = mapped_column(Float)
    estimated_time_hrs: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    mandi = relationship("Mandi", back_populates="transport_rates")

    __table_args__ = (
        UniqueConstraint("mandi_id", "from_location_name", name="uq_mandi_from_location"),
    )


# ─── Notification ───────────────────────────────────

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    farmer_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("farmers.id", ondelete="CASCADE")
    )
    channel: Mapped[NotificationChannel] = mapped_column(SAEnum(NotificationChannel))
    status: Mapped[NotificationStatus] = mapped_column(
        SAEnum(NotificationStatus), default=NotificationStatus.PENDING
    )
    message: Mapped[str] = mapped_column(Text)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    farmer = relationship("Farmer", back_populates="notifications")

    __table_args__ = (
        Index("ix_notif_farmer_created", "farmer_id", "created_at"),
    )


# ─── ModelVersion ───────────────────────────────────

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    version_tag: Mapped[str] = mapped_column(String(50), unique=True)
    model_type: Mapped[str] = mapped_column(String(50))
    metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    artifact_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    trained_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
