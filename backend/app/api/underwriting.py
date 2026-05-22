"""Underwriting calculation routes"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.services import underwriting_service, auth_service
from app.models.user import User

router = APIRouter()


class UnderwritingInput(BaseModel):
    purchase_price: float
    monthly_rent: float
    vacancy_rate: float = 0.05
    property_taxes_annual: float
    insurance_annual: float
    repairs_maintenance_annual: float = 0.0
    management_rate: float = 0.08
    capex_reserve_annual: float = 0.0
    down_payment_percent: float = 0.25
    interest_rate: float = 0.065
    loan_term_years: int = 30
    property_type: str = "single_family"


class UnderwritingResult(BaseModel):
    noi: float
    cap_rate: float
    cash_flow_monthly: float
    cash_flow_annual: float
    cash_on_cash_return: float
    dscr: float
    total_cash_invested: float
    break_even_occupancy: float
    deal_grade: str
    ai_verdict: str
    risk_flags: List[str]


class ProjectionYear(BaseModel):
    year: int
    property_value: float
    gross_income: float
    operating_expenses: float
    noi: float
    debt_service: float
    cash_flow: float
    loan_balance: float
    equity: float
    cash_on_cash: float


class ProjectionResult(BaseModel):
    projections: List[ProjectionYear]
    total_return: float
    irr: float
    equity_multiple: float


class ScenarioInput(BaseModel):
    scenario_name: str
    changed_inputs: Dict


class ScenarioResult(BaseModel):
    scenario_id: str
    scenario_name: str
    results: UnderwritingResult
    created_at: str


@router.post("/{deal_id}/underwrite", response_model=UnderwritingResult)
async def run_underwriting(
    deal_id: str,
    input_data: UnderwritingInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Run real estate underwriting calculations for a deal"""
    return await underwriting_service.run_underwriting(db, current_user, deal_id, input_data)


@router.get("/{deal_id}/results", response_model=UnderwritingResult)
async def get_underwriting_results(
    deal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Get latest underwriting results for a deal"""
    return await underwriting_service.get_underwriting_results(db, current_user, deal_id)


@router.post("/{deal_id}/projection", response_model=ProjectionResult)
async def run_projection(
    deal_id: str,
    years: int = 5,
    rent_growth_rate: float = 0.03,
    expense_growth_rate: float = 0.025,
    appreciation_rate: float = 0.03,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Run multi-year projection for a deal"""
    return await underwriting_service.run_projection(
        db,
        current_user,
        deal_id,
        years=years,
        rent_growth_rate=rent_growth_rate,
        expense_growth_rate=expense_growth_rate,
        appreciation_rate=appreciation_rate,
    )


@router.post("/{deal_id}/scenario", response_model=ScenarioResult)
async def create_scenario(
    deal_id: str,
    scenario: ScenarioInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Create a what-if scenario for a deal"""
    return await underwriting_service.create_scenario(
        db,
        current_user,
        deal_id,
        scenario.scenario_name,
        scenario.changed_inputs,
    )


@router.get("/{deal_id}/scenarios", response_model=List[ScenarioResult])
async def list_scenarios(
    deal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """List all scenarios for a deal"""
    return await underwriting_service.list_scenarios(db, current_user, deal_id)


@router.delete("/{deal_id}/scenario/{scenario_id}")
async def delete_scenario(
    deal_id: str,
    scenario_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Delete a scenario"""
    await underwriting_service.delete_scenario(db, current_user, deal_id, scenario_id)
    return {"message": "Scenario deleted successfully"}
