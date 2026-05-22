"""Document model for generated reports and documents"""

from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.utils.database import Base


class Document(Base):
    """Generated reports and documents for a deal"""
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    document_type = Column(String(50))  # summary, broker_email, investor_memo, lender_summary, etc
    title = Column(String(255), nullable=False)
    content = Column(Text)  # Document content
    pdf_url = Column(String(500))  # URL to PDF if generated
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Document {self.document_type}>"
