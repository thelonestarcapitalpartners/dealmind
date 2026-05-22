"""Scenario model for deal what-if analysis"""

from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from app.utils.database import Base


class Scenario(Base):
    """What-if scenario with modified assumptions and results"""
    __tablename__ = "scenarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)  # e.g., "Offer at $850k"
    changed_inputs = Column(JSONB)  # Only the fields that changed
    results_json = Column(JSONB)  # Full underwriting results for this scenario
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Scenario {self.name}>"
