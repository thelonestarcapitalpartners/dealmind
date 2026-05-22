"""Supabase-backed authentication service"""
from typing import Optional, Dict
from supabase import create_client, Client
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, Header
from jose import jwt, JWTError

from app.config.settings import settings
from app.models.user import User
from app.utils.database import get_db


_supabase: Optional[Client] = None


def get_supabase_client() -> Client:
    global _supabase
    if _supabase is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            # Supabase not configured - return None to allow local fallback
            return None
        _supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _supabase


async def signup(db: Session, email: str, password: str, full_name: str) -> Dict:
    """Sign up a new user with Supabase and create local user record."""
    supabase = get_supabase_client()

    # If Supabase is configured, use it
    if supabase is not None:
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
        except TypeError:
            res = supabase.auth.sign_up(email=email, password=password)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        if hasattr(res, "get") and res.get("error"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.get("error").get("message"))

        data = res.get("data") if isinstance(res, dict) else res
        access_token = None
        user_info = None
        if isinstance(data, dict):
            access_token = data.get("access_token") or data.get("session", {}).get("access_token")
            user_info = data.get("user") or data.get("session", {}).get("user")

        # Create local DB user if not exists
        if user_info and db is not None:
            existing = db.query(User).filter(User.email == email).first()
            if not existing:
                new_user = User(email=email, full_name=full_name)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                local_user = new_user
            else:
                local_user = existing
        else:
            local_user = None

        return {
            "access_token": access_token or "",
            "token_type": "bearer",
            "user_id": str(local_user.id) if local_user else "",
            "email": email,
        }

    # Local fallback when Supabase is not configured: create local user and issue JWT
    existing = db.query(User).filter(User.email == email).first()
    if not existing:
        new_user = User(email=email, full_name=full_name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        local_user = new_user
    else:
        local_user = existing

    # Create JWT token
    payload = {"email": email}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(local_user.id),
        "email": email,
    }


async def login(db: Session, email: str, password: str) -> Dict:
    """Authenticate user with Supabase and return tokens."""
    supabase = get_supabase_client()
    # If Supabase configured, use it
    if supabase is not None:
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        except AttributeError:
            try:
                res = supabase.auth.sign_in({"email": email, "password": password})
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        if hasattr(res, "get") and res.get("error"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.get("error").get("message"))

        data = res.get("data") if isinstance(res, dict) else res
        access_token = None
        user_info = None
        if isinstance(data, dict):
            access_token = data.get("access_token") or data.get("session", {}).get("access_token")
            user_info = data.get("user") or data.get("session", {}).get("user")

        if user_info and db is not None:
            existing = db.query(User).filter(User.email == email).first()
            if not existing:
                new_user = User(email=email, full_name=user_info.get("user_metadata", {}).get("full_name") or "")
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                local_user = new_user
            else:
                local_user = existing
        else:
            local_user = None

        return {
            "access_token": access_token or "",
            "token_type": "bearer",
            "user_id": str(local_user.id) if local_user else "",
            "email": email,
        }

    # Local fallback: issue JWT if user exists (or create)
    existing = db.query(User).filter(User.email == email).first()
    if not existing:
        # No password verification locally; just create user for testing
        new_user = User(email=email, full_name="")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        local_user = new_user
    else:
        local_user = existing

    token = jwt.encode({"email": email}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(local_user.id),
        "email": email,
    }


async def logout(access_token: str) -> bool:
    supabase = get_supabase_client()
    try:
        supabase.auth.sign_out()
        return True
    except Exception:
        return False


async def get_current_user_from_token(db: Session, access_token: str) -> Optional[User]:
    """Validate token with Supabase and return local User model."""
    if not access_token:
        return None

    supabase = get_supabase_client()
    user_resp = None
    try:
        user_resp = supabase.auth.get_user(access_token)
    except TypeError:
        try:
            user_resp = supabase.auth.get_user({"access_token": access_token})
        except Exception:
            user_resp = None
    except Exception:
        user_resp = None

    if isinstance(user_resp, dict) and user_resp.get("data"):
        u = user_resp.get("data").get("user")
        if u:
            email = u.get("email")
            return db.query(User).filter(User.email == email).first()

    # Fallback: attempt to decode JWT using local JWT secret (best-effort)
    try:
        payload = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email = payload.get("email")
    except JWTError:
        return None
    return db.query(User).filter(User.email == email).first()


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    token = authorization.split(" ")[-1]
    user = await get_current_user_from_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user
