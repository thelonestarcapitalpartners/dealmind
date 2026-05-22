"""Deal CRUD service for DealMind"""
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.deal import Deal, PropertyType, DealStatus
from app.models.user import User


def _get_deal(db: Session, user: User, deal_id: str) -> Deal:
    deal = db.query(Deal).filter(Deal.id == deal_id, Deal.user_id == user.id).first()
    if not deal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal not found")
    return deal


async def create_deal(db: Session, user: User, deal_data) -> Deal:
    try:
        property_type = PropertyType(deal_data.property_type)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid property type")

    deal = Deal(
        user_id=user.id,
        title=deal_data.title,
        address=deal_data.address,
        city=deal_data.city,
        state=deal_data.state,
        zip_code=deal_data.zip_code,
        property_type=property_type,
        unit_count=deal_data.unit_count,
        asking_price=deal_data.asking_price,
        source_type=deal_data.source_type,
        source_url=deal_data.source_url,
        status=DealStatus.DRAFT,
    )
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal


async def list_deals(db: Session, user: User) -> List[Deal]:
    return db.query(Deal).filter(Deal.user_id == user.id).order_by(Deal.created_at.desc()).all()


async def get_deal(db: Session, user: User, deal_id: str) -> Deal:
    return _get_deal(db, user, deal_id)


async def update_deal(db: Session, user: User, deal_id: str, deal_data) -> Deal:
    deal = _get_deal(db, user, deal_id)
    try:
        deal.property_type = PropertyType(deal_data.property_type)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid property type")

    deal.title = deal_data.title
    deal.address = deal_data.address
    deal.city = deal_data.city
    deal.state = deal_data.state
    deal.zip_code = deal_data.zip_code
    deal.unit_count = deal_data.unit_count
    deal.asking_price = deal_data.asking_price
    deal.source_type = deal_data.source_type
    deal.source_url = deal_data.source_url

    db.commit()
    db.refresh(deal)
    return deal


async def delete_deal(db: Session, user: User, deal_id: str) -> None:
    deal = _get_deal(db, user, deal_id)
    db.delete(deal)
    db.commit()
