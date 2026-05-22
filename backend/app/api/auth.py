"""Authentication API routes"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.services import auth_service

router = APIRouter()


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    subscription_plan: str
    monthly_deal_limit: int
    deals_used_this_month: int


@router.post("/signup", response_model=TokenResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **email**: User email address
    - **password**: User password
    - **full_name**: User's full name
    """
    result = await auth_service.signup(db, request.email, request.password, request.full_name)
    return TokenResponse(**result)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user
    
    - **email**: User email address
    - **password**: User password
    """
    result = await auth_service.login(db, request.email, request.password)
    return TokenResponse(**result)


@router.post("/logout")
async def logout():
    """Logout user"""
    return {"message": "Logged out (client-side)."}


@router.get("/me", response_model=UserResponse)
async def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    token = authorization.split(" ")[-1]
    user = await auth_service.get_current_user_from_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name or "",
        subscription_plan=user.subscription_plan.value,
        monthly_deal_limit=user.monthly_deal_limit,
        deals_used_this_month=user.deals_used_this_month,
    )
