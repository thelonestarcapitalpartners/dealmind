"""UnderwritingResult model for storing calculation results"""

from datetime import datetime
from sqlalchemy import Column, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from app.utils.database import Base


class UnderwritingResult(Base):
    """Results from underwriting calculations for a deal or scenario"""
    __tablename__ = "underwriting_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id = Column(UUID(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True)
    scenario_id = Column(UUID(as_uuid=True), nullable=True)  # Optional: results for a specific scenario
    
    # Key Metrics
    noi = Column(Float)  # Net Operating Income
    cap_rate = Column(Float)  # Cap Rate
    cash_flow_monthly = Column(Float)  # Monthly cash flow
    cash_flow_annual = Column(Float)  # Annual cash flow
    cash_on_cash = Column(Float)  # Cash-on-cash return
    dscr = Column(Float)  # Debt Service Coverage Ratio
    irr = Column(Float, nullable=True)  # Internal Rate of Return
    equity_multiple = Column(Float, nullable=True)  # Equity multiple
    break_even_occupancy = Column(Float)  # Break-even occupancy %
    total_cash_invested = Column(Float)  # Total cash required
    ltv = Column(Float, nullable=True)  # Loan-to-value ratio
    debt_yield = Column(Float, nullable=True)  # Debt yield
    
    # Full Results Object (includes all calculations)
    results_json = Column(JSONB)  # Complete results data
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<UnderwritingResult {self.deal_id}>"
