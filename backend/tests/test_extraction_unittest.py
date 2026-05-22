import unittest

from app.services.extraction_service import _simple_field_extract
from app.rules.us_rules import RulesEngine


class ExtractionTests(unittest.TestCase):
    def test_simple_field_extract(self):
        text = "Beautiful property listed at $1,250,000 with monthly rent $3,200 and vacancy 5% and taxes $4,500"
        out = _simple_field_extract(text)
        self.assertEqual(out.get('purchase_price'), 1250000.0)
        self.assertEqual(out.get('monthly_rent'), 3200.0)
        self.assertAlmostEqual(out.get('vacancy_rate'), 0.05)
        self.assertEqual(out.get('property_taxes_annual'), 4500.0)

    def test_rules_engine_recommendations_state(self):
        # Test that rules engine returns tax recommendation for known state
        recs = RulesEngine.apply_rules(state='TX', county=None, property_value=1000000)
        self.assertIn('property_taxes_annual', recs)
        self.assertIn('insurance_annual', recs)
        self.assertIn('repairs_maintenance_annual', recs)
        self.assertIn('capex_reserve_annual', recs)
        self.assertIsInstance(recs['property_taxes_annual']['value'], float)


if __name__ == '__main__':
    unittest.main()
