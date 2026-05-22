from app.services.extraction_service import _simple_field_extract


def test_simple_price_extraction():
    text = "Beautiful property listed at $1,250,000 with monthly rent $3,200 and vacancy 5% and taxes $4,500"
    out = _simple_field_extract(text)
    assert out.get("purchase_price") == 1250000.0
    assert out.get("monthly_rent") == 3200.0
    assert abs(out.get("vacancy_rate") - 0.05) < 1e-6
    assert out.get("property_taxes_annual") == 4500.0
