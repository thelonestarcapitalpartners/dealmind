"""Extraction service for URL, PDF, and image inputs."""
from __future__ import annotations
from typing import Dict, Any, Optional
from typing import TYPE_CHECKING
try:
    from fastapi import HTTPException, status
except Exception:
    class HTTPException(Exception):
        def __init__(self, status_code=None, detail=None):
            super().__init__(detail or "HTTPException")
            self.status_code = status_code

    class status:
        HTTP_404_NOT_FOUND = 404
        HTTP_400_BAD_REQUEST = 400
if TYPE_CHECKING:
    from sqlalchemy.orm import Session
import re
import io
# Defer heavy external imports into function scope to keep module lightweight for tests

from app.rules.us_rules import RulesEngine

# Delay importing heavy DB models until functions to allow lightweight testing


def _simple_field_extract(text: str) -> Dict[str, Any]:
    """Very simple heuristic extraction for numeric fields from text."""
    results: Dict[str, Any] = {}

    # Price: look for $ followed by numbers
    m = re.search(r"\$\s?([0-9,]{4,})", text)
    if m:
        price = float(m.group(1).replace(",", ""))
        results["purchase_price"] = price

    # Monthly rent: look for monthly rent patterns
    m = re.search(r"rent[:\s\$]*([0-9,]{3,})", text, re.IGNORECASE)
    if m:
        results["monthly_rent"] = float(m.group(1).replace(",", ""))

    # Vacancy rate
    m = re.search(r"vacancy[:\s]*([0-9]{1,2})%", text, re.IGNORECASE)
    if m:
        results["vacancy_rate"] = float(m.group(1)) / 100.0

    # Property taxes annual
    m = re.search(r"tax(es)?[:\s\$]*([0-9,]{3,})", text, re.IGNORECASE)
    if m:
        results["property_taxes_annual"] = float(m.group(2).replace(",", ""))

    return results


async def extract_from_url(db: Session, user: User, deal_id: str, url: str) -> Dict[str, Any]:
    from app.models.deal import Deal
    from app.models.deal_input import DealInput
    import requests
    from bs4 import BeautifulSoup

    deal: Optional[Deal] = db.query(Deal).filter(Deal.id == deal_id, Deal.user_id == user.id).first()
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to fetch URL: {e}")

    soup = BeautifulSoup(resp.text, "html.parser")
    texts = "\n".join([p.get_text(separator=" ") for p in soup.find_all(["p", "li", "span", "div"])])

    extracted = _simple_field_extract(texts)

    # Apply rules engine recommendations for missing fields
    recommendations = RulesEngine.apply_rules(
        state=deal.state or "",
        county=None,
        property_value=extracted.get("purchase_price", deal.asking_price or 0),
        property_taxes_annual=extracted.get("property_taxes_annual"),
        insurance_annual=extracted.get("insurance_annual"),
        repairs_maintenance_annual=extracted.get("repairs_maintenance_annual"),
    )

    # Persist DealInput
    raw = {
        "source": "url",
        "url": url,
        "text": texts[:20000],
    }
    deal_input = DealInput(
        deal_id=deal.id,
        input_data=raw,
        assumptions=recommendations,
        extracted_fields=extracted,
        confidence_scores={k: 0.7 for k in extracted.keys()},
    )
    db.add(deal_input)
    db.commit()
    db.refresh(deal_input)

    return {"extracted": extracted, "recommendations": recommendations, "deal_input_id": str(deal_input.id)}


async def extract_from_pdf(db: Session, user: User, deal_id: str, file_bytes: bytes) -> Dict[str, Any]:
    from app.models.deal import Deal
    from app.models.deal_input import DealInput
    import pdfplumber

    deal: Optional[Deal] = db.query(Deal).filter(Deal.id == deal_id, Deal.user_id == user.id).first()
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")

    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to read PDF: {e}")

    extracted = _simple_field_extract(full_text)

    recommendations = RulesEngine.apply_rules(
        state=deal.state or "",
        county=None,
        property_value=extracted.get("purchase_price", deal.asking_price or 0),
        property_taxes_annual=extracted.get("property_taxes_annual"),
        insurance_annual=extracted.get("insurance_annual"),
        repairs_maintenance_annual=extracted.get("repairs_maintenance_annual"),
    )

    raw = {"source": "pdf", "text": full_text[:20000]}
    deal_input = DealInput(
        deal_id=deal.id,
        input_data=raw,
        assumptions=recommendations,
        extracted_fields=extracted,
        confidence_scores={k: 0.75 for k in extracted.keys()},
    )
    db.add(deal_input)
    db.commit()
    db.refresh(deal_input)

    return {"extracted": extracted, "recommendations": recommendations, "deal_input_id": str(deal_input.id)}


async def extract_from_image(db: Session, user: User, deal_id: str, image_bytes: bytes) -> Dict[str, Any]:
    from app.models.deal import Deal
    from app.models.deal_input import DealInput
    from PIL import Image
    import pytesseract

    deal: Optional[Deal] = db.query(Deal).filter(Deal.id == deal_id, Deal.user_id == user.id).first()
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")

    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        text = pytesseract.image_to_string(img)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to process image: {e}")

    extracted = _simple_field_extract(text)

    recommendations = RulesEngine.apply_rules(
        state=deal.state or "",
        county=None,
        property_value=extracted.get("purchase_price", deal.asking_price or 0),
        property_taxes_annual=extracted.get("property_taxes_annual"),
        insurance_annual=extracted.get("insurance_annual"),
        repairs_maintenance_annual=extracted.get("repairs_maintenance_annual"),
    )

    raw = {"source": "image", "text": text[:20000]}
    deal_input = DealInput(
        deal_id=deal.id,
        input_data=raw,
        assumptions=recommendations,
        extracted_fields=extracted,
        confidence_scores={k: 0.65 for k in extracted.keys()},
    )
    db.add(deal_input)
    db.commit()
    db.refresh(deal_input)

    return {"extracted": extracted, "recommendations": recommendations, "deal_input_id": str(deal_input.id)}
