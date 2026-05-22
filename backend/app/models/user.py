"""User model for authentication and subscription management"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.utils.database import Base


class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    ELITE = "elite"
    ENTERPRISE = "enterprise"


class User(Base):
    """User account with subscription and deal limits"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False)
    monthly_deal_limit = Column(Integer, default=3)
    deals_used_this_month = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User {self.email} ({self.subscription_plan})>"
