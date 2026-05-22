"""Underwriting service for DealMind"""
from typing import Dict, List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.deal import Deal
from app.models.underwriting_result import UnderwritingResult
from app.models.scenario import Scenario
from app.models.user import User
from app.services.calculator import (
    UnderwritingCalculator,
    UnderwritingInput as CalculatorInput,
    ProjectionCalculator,
)


def _get_deal(db: Session, user: User, deal_id: str) -> Deal:
    deal = db.query(Deal).filter(Deal.id == deal_id, Deal.user_id == user.id).first()
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
    return deal


def _build_calculator_input(input_data) -> CalculatorInput:
    return CalculatorInput(
        purchase_price=input_data.purchase_price,
        monthly_rent=input_data.monthly_rent,
        vacancy_rate=input_data.vacancy_rate,
        property_taxes_annual=input_data.property_taxes_annual,
        insurance_annual=input_data.insurance_annual,
        repairs_maintenance_annual=input_data.repairs_maintenance_annual,
        management_rate=input_data.management_rate,
        capex_reserve_annual=input_data.capex_reserve_annual,
        utilities_annual=getattr(input_data, "utilities_annual", 0.0),
        hoa_monthly=getattr(input_data, "hoa_monthly", 0.0),
        other_expenses_annual=getattr(input_data, "other_expenses_annual", 0.0),
        down_payment_percent=input_data.down_payment_percent,
        interest_rate=input_data.interest_rate,
        loan_term_years=input_data.loan_term_years,
        amortization_years=getattr(input_data, "amortization_years", input_data.loan_term_years),
        property_type=input_data.property_type,
    )


def _serialize_output(output, ai_verdict: str) -> Dict:
    return {
        "noi": output.noi,
        "cap_rate": output.cap_rate,
        "cash_flow_monthly": output.cash_flow_monthly,
        "cash_flow_annual": output.cash_flow_annual,
        "cash_on_cash_return": output.cash_on_cash_return,
        "dscr": output.dscr,
        "total_cash_invested": output.total_cash_invested,
        "break_even_occupancy": output.break_even_occupancy,
        "deal_grade": output.deal_grade,
        "ai_verdict": ai_verdict,
        "risk_flags": output.risk_flags,
    }


def _build_results_json(input_data, output, ai_verdict: str) -> Dict:
    return {
        "inputs": input_data.dict() if hasattr(input_data, "dict") else {},
        "results": {
            "gross_scheduled_income": output.gross_scheduled_income,
            "vacancy_loss": output.vacancy_loss,
            "effective_gross_income": output.effective_gross_income,
            "management_expense": output.management_expense,
            "operating_expenses": output.operating_expenses,
            "noi": output.noi,
            "loan_amount": output.loan_amount,
            "monthly_debt_service": output.monthly_debt_service,
            "annual_debt_service": output.annual_debt_service,
            "cash_flow_annual": output.cash_flow_annual,
            "cash_flow_monthly": output.cash_flow_monthly,
            "cash_on_cash_return": output.cash_on_cash_return,
            "cap_rate": output.cap_rate,
            "dscr": output.dscr,
            "total_cash_invested": output.total_cash_invested,
            "ltv": output.ltv,
            "debt_yield": output.debt_yield,
            "break_even_occupancy": output.break_even_occupancy,
            "deal_grade": output.deal_grade,
            "risk_flags": output.risk_flags,
        },
        "ai_verdict": ai_verdict,
    }


def _generate_ai_verdict(output) -> str:
    verdict = (
        f"This deal is graded {output.deal_grade} with a {output.cap_rate * 100:.2f}% cap rate, "
        f"{output.dscr:.2f} DSCR, and ${output.cash_flow_monthly:,.0f} monthly cash flow."
    )
    if output.cash_flow_monthly < 0:
        verdict += " The deal generates negative cash flow and requires caution."
    return verdict


def _get_latest_result(db: Session, deal_id: str) -> Optional[UnderwritingResult]:
    return (
        db.query(UnderwritingResult)
        .filter(UnderwritingResult.deal_id == deal_id)
        .order_by(UnderwritingResult.created_at.desc())
        .first()
    )


def _calculate_irr(cash_flows: List[float]) -> float:
    def npv(rate: float) -> float:
        return sum(cf / ((1 + rate) ** idx) for idx, cf in enumerate(cash_flows))

    low, high = -0.99, 1.5
    if npv(low) * npv(high) > 0:
        return 0.0

    for _ in range(80):
        mid = (low + high) / 2
        if npv(mid) > 0:
            low = mid
        else:
            high = mid
    return mid


async def run_underwriting(db: Session, user: User, deal_id: str, input_data) -> Dict:
    deal = _get_deal(db, user, deal_id)
    calc_input = _build_calculator_input(input_data)
    output = UnderwritingCalculator.calculate(calc_input)
    ai_verdict = _generate_ai_verdict(output)
    serialized = _serialize_output(output, ai_verdict)
    result_json = _build_results_json(input_data, output, ai_verdict)

    underwriting_result = UnderwritingResult(
        deal_id=deal.id,
        noi=output.noi,
        cap_rate=output.cap_rate,
        cash_flow_monthly=output.cash_flow_monthly,
        cash_flow_annual=output.cash_flow_annual,
        cash_on_cash=output.cash_on_cash_return,
        dscr=output.dscr,
        irr=None,
        equity_multiple=None,
        break_even_occupancy=output.break_even_occupancy,
        total_cash_invested=output.total_cash_invested,
        ltv=output.ltv,
        debt_yield=output.debt_yield,
        results_json=result_json,
    )
    db.add(underwriting_result)

    deal.deal_grade = output.deal_grade
    deal.ai_verdict = ai_verdict
    db.commit()
    db.refresh(underwriting_result)

    return serialized


async def get_underwriting_results(db: Session, user: User, deal_id: str) -> Dict:
    _get_deal(db, user, deal_id)
    result = _get_latest_result(db, deal_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No underwriting results found")

    results = result.results_json.get("results", {})
    return {
        "noi": results.get("noi", 0.0),
        "cap_rate": results.get("cap_rate", 0.0),
        "cash_flow_monthly": results.get("cash_flow_monthly", 0.0),
        "cash_flow_annual": results.get("cash_flow_annual", 0.0),
        "cash_on_cash_return": results.get("cash_on_cash_return", 0.0),
        "dscr": results.get("dscr", 0.0),
        "total_cash_invested": results.get("total_cash_invested", 0.0),
        "break_even_occupancy": results.get("break_even_occupancy", 0.0),
        "deal_grade": results.get("deal_grade", "N/A"),
        "ai_verdict": result.results_json.get("ai_verdict", ""),
        "risk_flags": results.get("risk_flags", []),
    }


async def run_projection(
    db: Session,
    user: User,
    deal_id: str,
    years: int = 5,
    rent_growth_rate: float = 0.03,
    expense_growth_rate: float = 0.025,
    appreciation_rate: float = 0.03,
) -> Dict:
    _get_deal(db, user, deal_id)
    result = _get_latest_result(db, deal_id)
    if not result or not result.results_json:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No underwriting data available for projections")

    base_inputs = result.results_json.get("inputs")
    if not base_inputs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Underwriting input assumptions are missing")

    calc_input = CalculatorInput(
        purchase_price=base_inputs.get("purchase_price", 0.0),
        monthly_rent=base_inputs.get("monthly_rent", 0.0),
        vacancy_rate=base_inputs.get("vacancy_rate", 0.05),
        property_taxes_annual=base_inputs.get("property_taxes_annual", 0.0),
        insurance_annual=base_inputs.get("insurance_annual", 0.0),
        repairs_maintenance_annual=base_inputs.get("repairs_maintenance_annual", 0.0),
        management_rate=base_inputs.get("management_rate", 0.08),
        capex_reserve_annual=base_inputs.get("capex_reserve_annual", 0.0),
        utilities_annual=base_inputs.get("utilities_annual", 0.0),
        hoa_monthly=base_inputs.get("hoa_monthly", 0.0),
        other_expenses_annual=base_inputs.get("other_expenses_annual", 0.0),
        down_payment_percent=base_inputs.get("down_payment_percent", 0.25),
        interest_rate=base_inputs.get("interest_rate", 0.065),
        loan_term_years=base_inputs.get("loan_term_years", 30),
        amortization_years=base_inputs.get("amortization_years", base_inputs.get("loan_term_years", 30)),
        property_type=base_inputs.get("property_type", "single_family"),
    )

    projections = ProjectionCalculator.project(
        calc_input,
        years=years,
        rent_growth_rate=rent_growth_rate,
        expense_growth_rate=expense_growth_rate,
        appreciation_rate=appreciation_rate,
    )

    projection_rows = [
        {
            "year": p.year,
            "property_value": p.property_value,
            "gross_income": p.gross_income,
            "operating_expenses": p.operating_expenses,
            "noi": p.noi,
            "debt_service": p.debt_service,
            "cash_flow": p.cash_flow,
            "loan_balance": p.loan_balance,
            "equity": p.equity,
            "cash_on_cash": p.cash_on_cash,
        }
        for p in projections
    ]

    initial_equity = calc_input.purchase_price * calc_input.down_payment_percent
    total_cash_flow = sum(p["cash_flow"] for p in projection_rows)
    final_equity = projection_rows[-1]["equity"] if projection_rows else 0.0
    total_profit = total_cash_flow + final_equity
    total_return = total_profit / initial_equity if initial_equity > 0 else 0.0
    equity_multiple = (total_profit + initial_equity) / initial_equity if initial_equity > 0 else 0.0

    cash_flows = [-initial_equity] + [row["cash_flow"] for row in projection_rows]
    if projection_rows:
        cash_flows[-1] += final_equity
    irr = _calculate_irr(cash_flows)

    return {
        "projections": projection_rows,
        "total_return": total_return,
        "irr": irr,
        "equity_multiple": equity_multiple,
    }


async def create_scenario(db: Session, user: User, deal_id: str, scenario_name: str, changed_inputs: Dict) -> Dict:
    _get_deal(db, user, deal_id)
    result = _get_latest_result(db, deal_id)
    if not result or not result.results_json:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Need existing underwriting data to create a scenario")

    base_inputs = result.results_json.get("inputs", {})
    scenario_inputs = {**base_inputs, **changed_inputs}
    calc_input = CalculatorInput(
        purchase_price=scenario_inputs.get("purchase_price", 0.0),
        monthly_rent=scenario_inputs.get("monthly_rent", 0.0),
        vacancy_rate=scenario_inputs.get("vacancy_rate", 0.05),
        property_taxes_annual=scenario_inputs.get("property_taxes_annual", 0.0),
        insurance_annual=scenario_inputs.get("insurance_annual", 0.0),
        repairs_maintenance_annual=scenario_inputs.get("repairs_maintenance_annual", 0.0),
        management_rate=scenario_inputs.get("management_rate", 0.08),
        capex_reserve_annual=scenario_inputs.get("capex_reserve_annual", 0.0),
        utilities_annual=scenario_inputs.get("utilities_annual", 0.0),
        hoa_monthly=scenario_inputs.get("hoa_monthly", 0.0),
        other_expenses_annual=scenario_inputs.get("other_expenses_annual", 0.0),
        down_payment_percent=scenario_inputs.get("down_payment_percent", 0.25),
        interest_rate=scenario_inputs.get("interest_rate", 0.065),
        loan_term_years=scenario_inputs.get("loan_term_years", 30),
        amortization_years=scenario_inputs.get("amortization_years", scenario_inputs.get("loan_term_years", 30)),
        property_type=scenario_inputs.get("property_type", "single_family"),
    )

    output = UnderwritingCalculator.calculate(calc_input)
    ai_verdict = _generate_ai_verdict(output)
    results_json = _build_results_json(calc_input, output, ai_verdict)

    scenario = Scenario(
        deal_id=deal_id,
        name=scenario_name,
        changed_inputs=changed_inputs,
        results_json=results_json,
    )
    db.add(scenario)
    db.commit()
    db.refresh(scenario)

    return {
        "scenario_id": str(scenario.id),
        "scenario_name": scenario.name,
        "results": _serialize_output(output, ai_verdict),
        "created_at": scenario.created_at.isoformat(),
    }


async def list_scenarios(db: Session, user: User, deal_id: str) -> List[Dict]:
    _get_deal(db, user, deal_id)
    scenarios = (
        db.query(Scenario)
        .filter(Scenario.deal_id == deal_id)
        .order_by(Scenario.created_at.desc())
        .all()
    )
    return [
        {
            "scenario_id": str(s.id),
            "scenario_name": s.name,
            "results": s.results_json.get("results", {}),
            "created_at": s.created_at.isoformat(),
        }
        for s in scenarios
    ]


async def delete_scenario(db: Session, user: User, deal_id: str, scenario_id: str) -> None:
    _get_deal(db, user, deal_id)
    scenario = (
        db.query(Scenario)
        .filter(Scenario.id == scenario_id, Scenario.deal_id == deal_id)
        .first()
    )
    if not scenario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
    db.delete(scenario)
    db.commit()
