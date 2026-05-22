"""Deal model for real estate properties"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
import enum

from app.utils.database import Base


class PropertyType(str, enum.Enum):
    SINGLE_FAMILY = "single_family"
    CONDO = "condo"
    DUPLEX = "duplex"
    TRIPLEX = "triplex"
    FOURPLEX = "fourplex"
    SMALL_MULTIFAMILY = "small_multifamily"
    COMMERCIAL_MULTIFAMILY = "commercial_multifamily"
    RETAIL = "retail"
    OFFICE = "office"
    INDUSTRIAL = "industrial"
    LAND = "land"
    MIXED_USE = "mixed_use"


class DealStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class Deal(Base):
    """Real estate deal with property and financial information"""
    __tablename__ = "deals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Basic Info
    title = Column(String(255), nullable=False)
    source_type = Column(String(50))  # url, pdf, image, manual
    source_url = Column(String(500))
    
    # Location
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    zip_code = Column(String(20))
    country = Column(String(100), default="US")
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Property Details
    property_type = Column(Enum(PropertyType), nullable=False)
    unit_count = Column(Integer)
    
    # Financials
    asking_price = Column(Float)
    
    # Analysis Results
    status = Column(Enum(DealStatus), default=DealStatus.DRAFT)
    deal_grade = Column(String(5))  # A+, A, B, C, D, F
    ai_verdict = Column(Text)  # One-sentence verdict
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Deal {self.title} ({self.property_type})>"
