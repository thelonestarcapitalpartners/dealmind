"""Rules engine for country/state specific assumptions"""

from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class LocationRules:
    """Rules and defaults for a specific location"""
    property_tax_rate: Optional[float] = None  # As % of property value
    property_tax_fixed: Optional[float] = None  # Fixed annual amount
    insurance_rate: Optional[float] = None  # As % of property value
    insurance_fixed: Optional[float] = None  # Fixed annual amount
    repairs_maintenance_rate: float = 0.01  # % of property value
    capex_reserve_rate: float = 0.01  # % of property value
    default_vacancy_rate: float = 0.05
    default_management_rate: float = 0.08
    depreciation_rate: Optional[float] = None  # For tax purposes
    name: str = ""


class RulesEngine:
    """Lookup and apply location-specific rules"""
    
    # US Federal defaults
    US_FEDERAL_RULES = LocationRules(
        name="US Federal Defaults",
        repairs_maintenance_rate=0.01,
        capex_reserve_rate=0.01,
        default_vacancy_rate=0.05,
        default_management_rate=0.08,
        depreciation_rate=0.0364,  # 27.5 years for residential
    )
    
    # Texas specific
    TEXAS_RULES = LocationRules(
        name="Texas",
        repairs_maintenance_rate=0.01,
        capex_reserve_rate=0.01,
        default_vacancy_rate=0.05,
        default_management_rate=0.08,
        depreciation_rate=0.0364,
        # Note: TX property taxes vary widely by county (0.6-2.5%)
    )
    
    # California specific
    CALIFORNIA_RULES = LocationRules(
        name="California",
        repairs_maintenance_rate=0.01,
        capex_reserve_rate=0.01,
        default_vacancy_rate=0.06,  # Higher vacancy in CA
        default_management_rate=0.10,  # Higher management costs
        depreciation_rate=0.0364,
    )
    
    # Florida specific
    FLORIDA_RULES = LocationRules(
        name="Florida",
        repairs_maintenance_rate=0.015,  # Higher due to hurricanes
        capex_reserve_rate=0.015,
        default_vacancy_rate=0.08,  # Higher turnover
        default_management_rate=0.10,
        depreciation_rate=0.0364,
    )
    
    # New York specific
    NEW_YORK_RULES = LocationRules(
        name="New York",
        repairs_maintenance_rate=0.01,
        capex_reserve_rate=0.01,
        default_vacancy_rate=0.05,
        default_management_rate=0.12,  # Higher management costs in NYC
        depreciation_rate=0.0364,
    )
    
    # County tax rates (simplified - these would normally come from a database)
    PROPERTY_TAX_RATES = {
        # Texas counties
        "TX_TRAVIS": 0.0076,  # Austin area
        "TX_HARRIS": 0.0081,  # Houston area
        "TX_DALLAS": 0.0074,  # Dallas area
        "TX_TARRANT": 0.0080,  # Fort Worth area
        "TX_BEXAR": 0.0080,  # San Antonio area
        
        # California counties
        "CA_LOS_ANGELES": 0.0076,
        "CA_SAN_DIEGO": 0.0075,
        "CA_SANTA_CLARA": 0.0078,
        "CA_ALAMEDA": 0.0080,
        
        # Florida counties
        "FL_MIAMI_DADE": 0.0083,
        "FL_BROWARD": 0.0085,
        "FL_HILLSBOROUGH": 0.0089,
        
        # New York
        "NY_NEW_YORK": 0.0171,  # NYC is very high
        "NY_WESTCHESTER": 0.0185,
    }
    
    # Insurance rates as % of property value
    INSURANCE_RATES = {
        "TX": 0.006,
        "CA": 0.007,
        "FL": 0.010,  # Hurricane risk
        "NY": 0.008,
        "US_DEFAULT": 0.007,
    }
    
    @staticmethod
    def get_state_rules(state: str) -> LocationRules:
        """Get rules for a US state"""
        state = state.upper()
        
        rules_map = {
            "TX": RulesEngine.TEXAS_RULES,
            "CA": RulesEngine.CALIFORNIA_RULES,
            "FL": RulesEngine.FLORIDA_RULES,
            "NY": RulesEngine.NEW_YORK_RULES,
        }
        
        return rules_map.get(state, RulesEngine.US_FEDERAL_RULES)
    
    @staticmethod
    def get_property_tax_rate(state: str, county: Optional[str] = None) -> Optional[float]:
        """Get property tax rate for location"""
        if county and state:
            county_key = f"{state.upper()}_{county.upper()}"
            return RulesEngine.PROPERTY_TAX_RATES.get(county_key)
        
        # Default to None if county-specific not found
        return None
    
    @staticmethod
    def get_insurance_rate(state: str) -> float:
        """Get insurance rate as % of property value"""
        state = state.upper()
        return RulesEngine.INSURANCE_RATES.get(state, RulesEngine.INSURANCE_RATES["US_DEFAULT"])
    
    @staticmethod
    def apply_rules(
        state: str,
        county: Optional[str] = None,
        repairs_maintenance_annual: Optional[float] = None,
        property_taxes_annual: Optional[float] = None,
        insurance_annual: Optional[float] = None,
        property_value: float = 0,
    ) -> Dict:
        """
        Apply location rules to fill in missing assumptions
        
        Returns dict with recommendations for missing values
        """
        rules = RulesEngine.get_state_rules(state)
        recommendations = {}
        
        # Property Taxes
        if property_taxes_annual is None or property_taxes_annual == 0:
            if county:
                rate = RulesEngine.get_property_tax_rate(state, county)
                if rate:
                    recommended_taxes = property_value * rate
                    recommendations["property_taxes_annual"] = {
                        "value": recommended_taxes,
                        "source": f"County rate {rate*100:.2f}%",
                        "confidence": 0.9,
                    }
            # Fallback to state average if no county rate
            if "property_taxes_annual" not in recommendations:
                # These are rough state averages
                state_averages = {
                    "TX": property_value * 0.0078,
                    "CA": property_value * 0.0077,
                    "FL": property_value * 0.0086,
                    "NY": property_value * 0.0180,
                }
                if state.upper() in state_averages:
                    recommendations["property_taxes_annual"] = {
                        "value": state_averages[state.upper()],
                        "source": f"State average",
                        "confidence": 0.7,
                    }
        
        # Insurance
        if insurance_annual is None or insurance_annual == 0:
            insurance_rate = RulesEngine.get_insurance_rate(state)
            recommended_insurance = property_value * insurance_rate
            recommendations["insurance_annual"] = {
                "value": recommended_insurance,
                "source": f"State rate {insurance_rate*100:.1f}%",
                "confidence": 0.8,
            }
        
        # Repairs & Maintenance
        if repairs_maintenance_annual is None or repairs_maintenance_annual == 0:
            recommended_repairs = property_value * rules.repairs_maintenance_rate
            recommendations["repairs_maintenance_annual"] = {
                "value": recommended_repairs,
                "source": f"Standard rate {rules.repairs_maintenance_rate*100:.1f}%",
                "confidence": 0.7,
            }
        
        # CapEx Reserve
        capex_rate = rules.capex_reserve_rate
        recommended_capex = property_value * capex_rate
        recommendations["capex_reserve_annual"] = {
            "value": recommended_capex,
            "source": f"Standard rate {capex_rate*100:.1f}%",
            "confidence": 0.8,
        }
        
        return recommendations
