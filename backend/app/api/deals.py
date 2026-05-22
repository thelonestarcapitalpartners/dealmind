"""Deals API routes"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.services import deal_service, auth_service
from app.services import extraction_service
from fastapi import UploadFile, File
from app.models.user import User

router = APIRouter()


class DealCreate(BaseModel):
    title: str
    address: str
    city: str
    state: str
    zip_code: str
    property_type: str
    unit_count: int
    asking_price: float
    source_type: str  # url, pdf, image, manual
    source_url: Optional[str] = None


class DealResponse(BaseModel):
    id: str
    title: str
    address: str
    city: str
    state: str
    zip_code: str
    property_type: str
    unit_count: int
    asking_price: float
    deal_grade: Optional[str] = None
    ai_verdict: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime


@router.post("", response_model=DealResponse)
async def create_deal(
    deal: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Create a new deal"""
    created = await deal_service.create_deal(db, current_user, deal)
    return DealResponse(
        id=str(created.id),
        title=created.title,
        address=created.address,
        city=created.city,
        state=created.state,
        zip_code=created.zip_code,
        property_type=created.property_type.value,
        unit_count=created.unit_count,
        asking_price=created.asking_price,
        deal_grade=created.deal_grade,
        ai_verdict=created.ai_verdict,
        status=created.status.value,
        created_at=created.created_at,
        updated_at=created.updated_at,
    )


@router.get("", response_model=List[DealResponse])
async def list_deals(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """List all deals for current user"""
    deals = await deal_service.list_deals(db, current_user)
    return [
        DealResponse(
            id=str(item.id),
            title=item.title,
            address=item.address,
            city=item.city,
            state=item.state,
            zip_code=item.zip_code,
            property_type=item.property_type.value,
            unit_count=item.unit_count,
            asking_price=item.asking_price,
            deal_grade=item.deal_grade,
            ai_verdict=item.ai_verdict,
            status=item.status.value,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        for item in deals
    ]


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Get a specific deal"""
    item = await deal_service.get_deal(db, current_user, deal_id)
    return DealResponse(
        id=str(item.id),
        title=item.title,
        address=item.address,
        city=item.city,
        state=item.state,
        zip_code=item.zip_code,
        property_type=item.property_type.value,
        unit_count=item.unit_count,
        asking_price=item.asking_price,
        deal_grade=item.deal_grade,
        ai_verdict=item.ai_verdict,
        status=item.status.value,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.patch("/{deal_id}", response_model=DealResponse)
async def update_deal(
    deal_id: str,
    deal: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Update a deal"""
    updated = await deal_service.update_deal(db, current_user, deal_id, deal)
    return DealResponse(
        id=str(updated.id),
        title=updated.title,
        address=updated.address,
        city=updated.city,
        state=updated.state,
        zip_code=updated.zip_code,
        property_type=updated.property_type.value,
        unit_count=updated.unit_count,
        asking_price=updated.asking_price,
        deal_grade=updated.deal_grade,
        ai_verdict=updated.ai_verdict,
        status=updated.status.value,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
    )


@router.delete("/{deal_id}")
async def delete_deal(
    deal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Delete a deal"""
    await deal_service.delete_deal(db, current_user, deal_id)
    return {"message": "Deal deleted successfully"}


@router.post("/{deal_id}/from-url")
async def create_deal_from_url(deal_id: str, url: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """Extract deal data from property URL"""
    return await extraction_service.extract_from_url(db, current_user, deal_id, url)


@router.post("/{deal_id}/from-pdf")
async def create_deal_from_pdf(
    deal_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Extract deal data from PDF upload"""
    content = await file.read()
    return await extraction_service.extract_from_pdf(db, current_user, deal_id, content)


@router.post("/{deal_id}/from-image")
async def create_deal_from_image(
    deal_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Extract deal data from image upload"""
    content = await file.read()
    return await extraction_service.extract_from_image(db, current_user, deal_id, content)
