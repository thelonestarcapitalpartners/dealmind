"""Core underwriting calculation engine - deterministic real estate math"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from decimal import Decimal
import math


@dataclass
class UnderwritingInput:
    """Input assumptions for underwriting"""
    purchase_price: float
    monthly_rent: float
    vacancy_rate: float = 0.05
    property_taxes_annual: float = 0.0
    insurance_annual: float = 0.0
    repairs_maintenance_annual: float = 0.0
    management_rate: float = 0.08  # % of gross income
    capex_reserve_annual: float = 0.0
    utilities_annual: float = 0.0
    hoa_monthly: float = 0.0
    other_expenses_annual: float = 0.0
    down_payment_percent: float = 0.25
    interest_rate: float = 0.065
    loan_term_years: int = 30
    amortization_years: int = 30


@dataclass
class UnderwritingOutput:
    """Complete underwriting calculation results"""
    # Income
    gross_scheduled_income: float
    vacancy_loss: float
    effective_gross_income: float
    
    # Expenses
    management_expense: float
    operating_expenses: float
    
    # NOI
    noi: float
    
    # Financing
    loan_amount: float
    monthly_debt_service: float
    annual_debt_service: float
    
    # Cash Flow
    cash_flow_annual: float
    cash_flow_monthly: float
    
    # Returns
    cash_on_cash_return: float
    cap_rate: float
    dscr: float
    break_even_occupancy: float
    total_cash_invested: float
    ltv: float
    debt_yield: float
    
    # Risk
    deal_grade: str
    risk_flags: List[str]


class UnderwritingCalculator:
    """Core real estate underwriting calculations"""
    
    @staticmethod
    def calculate(inputs: UnderwritingInput) -> UnderwritingOutput:
        """Run complete underwriting analysis"""
        
        # Income Calculations
        gross_scheduled_income = UnderwritingCalculator._calculate_gsi(inputs)
        vacancy_loss = UnderwritingCalculator._calculate_vacancy_loss(gross_scheduled_income, inputs.vacancy_rate)
        effective_gross_income = gross_scheduled_income - vacancy_loss
        
        # Expense Calculations
        management_expense = effective_gross_income * inputs.management_rate
        operating_expenses = UnderwritingCalculator._calculate_operating_expenses(inputs, management_expense)
        
        # NOI
        noi = effective_gross_income - operating_expenses
        
        # Financing
        loan_amount = inputs.purchase_price * (1 - inputs.down_payment_percent)
        monthly_debt_service = UnderwritingCalculator._calculate_monthly_debt_service(
            loan_amount,
            inputs.interest_rate,
            inputs.amortization_years
        )
        annual_debt_service = monthly_debt_service * 12
        
        # Cash Flow
        cash_flow_annual = noi - annual_debt_service
        cash_flow_monthly = cash_flow_annual / 12
        
        # Returns
        total_cash_invested = inputs.purchase_price * inputs.down_payment_percent
        cash_on_cash_return = cash_flow_annual / total_cash_invested if total_cash_invested > 0 else 0
        cap_rate = noi / inputs.purchase_price if inputs.purchase_price > 0 else 0
        dscr = noi / annual_debt_service if annual_debt_service > 0 else 0
        ltv = loan_amount / inputs.purchase_price if inputs.purchase_price > 0 else 0
        debt_yield = noi / loan_amount if loan_amount > 0 else 0
        break_even_occupancy = (operating_expenses + annual_debt_service) / gross_scheduled_income if gross_scheduled_income > 0 else 0
        
        # Grade and Risk Assessment
        deal_grade, risk_flags = UnderwritingCalculator._assess_deal(
            cap_rate, dscr, cash_on_cash_return, cash_flow_monthly, break_even_occupancy
        )
        
        return UnderwritingOutput(
            gross_scheduled_income=gross_scheduled_income,
            vacancy_loss=vacancy_loss,
            effective_gross_income=effective_gross_income,
            management_expense=management_expense,
            operating_expenses=operating_expenses,
            noi=noi,
            loan_amount=loan_amount,
            monthly_debt_service=monthly_debt_service,
            annual_debt_service=annual_debt_service,
            cash_flow_annual=cash_flow_annual,
            cash_flow_monthly=cash_flow_monthly,
            cash_on_cash_return=cash_on_cash_return,
            cap_rate=cap_rate,
            dscr=dscr,
            break_even_occupancy=break_even_occupancy,
            total_cash_invested=total_cash_invested,
            ltv=ltv,
            debt_yield=debt_yield,
            deal_grade=deal_grade,
            risk_flags=risk_flags,
        )
    
    @staticmethod
    def _calculate_gsi(inputs: UnderwritingInput) -> float:
        """Gross Scheduled Income = monthly_rent * 12"""
        return inputs.monthly_rent * 12
    
    @staticmethod
    def _calculate_vacancy_loss(gsi: float, vacancy_rate: float) -> float:
        """Vacancy Loss = GSI * vacancy_rate"""
        return gsi * vacancy_rate
    
    @staticmethod
    def _calculate_operating_expenses(inputs: UnderwritingInput, management_expense: float) -> float:
        """Total operating expenses"""
        return (
            inputs.property_taxes_annual +
            inputs.insurance_annual +
            inputs.repairs_maintenance_annual +
            management_expense +
            inputs.capex_reserve_annual +
            inputs.utilities_annual +
            (inputs.hoa_monthly * 12) +
            inputs.other_expenses_annual
        )
    
    @staticmethod
    def _calculate_monthly_debt_service(loan_amount: float, annual_rate: float, years: int) -> float:
        """
        Calculate monthly debt service using amortization formula
        
        Formula: P * [r(1+r)^n] / [(1+r)^n - 1]
        where:
        P = principal (loan amount)
        r = monthly interest rate
        n = number of payments
        """
        if loan_amount <= 0 or years <= 0:
            return 0
        
        monthly_rate = annual_rate / 12
        if monthly_rate == 0:
            return loan_amount / (years * 12)
        
        num_payments = years * 12
        numerator = monthly_rate * (1 + monthly_rate) ** num_payments
        denominator = (1 + monthly_rate) ** num_payments - 1
        
        return loan_amount * (numerator / denominator)
    
    @staticmethod
    def _assess_deal(
        cap_rate: float,
        dscr: float,
        cash_on_cash: float,
        monthly_cash_flow: float,
        break_even_occupancy: float
    ) -> tuple:
        """
        Assess deal quality and return grade + risk flags
        
        Grade factors:
        - Cap Rate (target 5-10%)
        - DSCR (minimum 1.0, good 1.25+)
        - Cash-on-Cash (target 8%+)
        - Monthly Cash Flow (positive is good)
        - Break-even Occupancy (lower is better, 70% or less is good)
        """
        risk_flags = []
        grade_score = 0
        
        # Cap Rate Assessment (25 points max)
        if cap_rate >= 0.10:
            grade_score += 25
        elif cap_rate >= 0.08:
            grade_score += 20
        elif cap_rate >= 0.06:
            grade_score += 15
        elif cap_rate >= 0.04:
            grade_score += 10
        else:
            grade_score += 5
            risk_flags.append("Cap rate below 4%")
        
        # DSCR Assessment (25 points max)
        if dscr >= 1.40:
            grade_score += 25
        elif dscr >= 1.25:
            grade_score += 20
        elif dscr >= 1.10:
            grade_score += 15
        elif dscr >= 1.0:
            grade_score += 10
        else:
            grade_score += 0
            risk_flags.append("DSCR below 1.0 - lender red flag")
        
        # Cash-on-Cash Assessment (25 points max)
        if cash_on_cash >= 0.12:
            grade_score += 25
        elif cash_on_cash >= 0.08:
            grade_score += 20
        elif cash_on_cash >= 0.04:
            grade_score += 15
        else:
            grade_score += 5
            risk_flags.append("Low cash-on-cash return")
        
        # Cash Flow Assessment (15 points max)
        if monthly_cash_flow >= 500:
            grade_score += 15
        elif monthly_cash_flow >= 0:
            grade_score += 10
        else:
            grade_score += 0
            risk_flags.append("Negative monthly cash flow")
        
        # Break-even Occupancy (10 points max)
        if break_even_occupancy <= 0.65:
            grade_score += 10
        elif break_even_occupancy <= 0.75:
            grade_score += 5
        else:
            risk_flags.append("High break-even occupancy")
        
        # Convert score to grade
        if grade_score >= 95:
            grade = "A+"
        elif grade_score >= 85:
            grade = "A"
        elif grade_score >= 75:
            grade = "B"
        elif grade_score >= 65:
            grade = "C"
        elif grade_score >= 50:
            grade = "D"
        else:
            grade = "F"
        
        return grade, risk_flags


@dataclass
class ProjectionYear:
    """Single year projection"""
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


class ProjectionCalculator:
    """Multi-year projection calculations"""
    
    @staticmethod
    def project(
        inputs: UnderwritingInput,
        years: int = 5,
        rent_growth_rate: float = 0.03,
        expense_growth_rate: float = 0.025,
        appreciation_rate: float = 0.03
    ) -> List[ProjectionYear]:
        """Generate multi-year projection"""
        
        projections = []
        current_property_value = inputs.purchase_price
        current_monthly_rent = inputs.monthly_rent
        current_property_taxes = inputs.property_taxes_annual
        current_insurance = inputs.insurance_annual
        current_repairs = inputs.repairs_maintenance_annual
        
        # Initial loan amount and balance
        loan_amount = inputs.purchase_price * (1 - inputs.down_payment_percent)
        loan_balance = loan_amount
        monthly_debt_service = UnderwritingCalculator._calculate_monthly_debt_service(
            loan_amount,
            inputs.interest_rate,
            inputs.amortization_years
        )
        
        for year in range(1, years + 1):
            # Update values based on growth rates
            current_monthly_rent *= (1 + rent_growth_rate)
            current_property_value *= (1 + appreciation_rate)
            current_property_taxes *= (1 + expense_growth_rate)
            current_insurance *= (1 + expense_growth_rate)
            current_repairs *= (1 + expense_growth_rate)
            
            # Income
            gross_income = current_monthly_rent * 12
            vacancy_loss = gross_income * inputs.vacancy_rate
            effective_income = gross_income - vacancy_loss
            
            # Expenses
            management_expense = effective_income * inputs.management_rate
            operating_expenses = (
                current_property_taxes +
                current_insurance +
                current_repairs +
                management_expense +
                inputs.capex_reserve_annual +
                inputs.utilities_annual +
                (inputs.hoa_monthly * 12) +
                inputs.other_expenses_annual
            )
            
            # NOI
            noi = effective_income - operating_expenses
            
            # Debt Service
            annual_debt_service = monthly_debt_service * 12
            
            # Cash Flow
            cash_flow = noi - annual_debt_service
            
            # Loan Balance (reduce with each payment)
            monthly_interest = loan_balance * (inputs.interest_rate / 12)
            monthly_principal = monthly_debt_service - monthly_interest
            loan_balance = max(0, loan_balance - (monthly_principal * 12))
            
            # Equity
            equity = current_property_value - loan_balance
            
            # Cash on Cash
            total_cash_invested = inputs.purchase_price * inputs.down_payment_percent
            cash_on_cash = cash_flow / total_cash_invested if total_cash_invested > 0 else 0
            
            projections.append(ProjectionYear(
                year=year,
                property_value=current_property_value,
                gross_income=gross_income,
                operating_expenses=operating_expenses,
                noi=noi,
                debt_service=annual_debt_service,
                cash_flow=cash_flow,
                loan_balance=loan_balance,
                equity=equity,
                cash_on_cash=cash_on_cash,
            ))
        
        return projections
