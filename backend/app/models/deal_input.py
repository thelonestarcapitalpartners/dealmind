"""DealInput model for storing extracted data and assumptions"""

from datetime import datetime
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from app.utils.database import Base


class DealInput(Base):
    """Raw input data, extracted fields, and user assumptions for a deal"""
    __tablename__ = "deal_inputs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Raw input
    input_data = Column(JSONB)  # Original URL, PDF text, or manual entry
    
    # Extracted and Processed
    assumptions = Column(JSONB)  # User-confirmed assumptions
    extracted_fields = Column(JSONB)  # All extracted property/financial data
    confidence_scores = Column(JSONB)  # Confidence per field
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<DealInput {self.deal_id}>"
