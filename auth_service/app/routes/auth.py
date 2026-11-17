from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app.models.user import User, RefreshToken
from app.schemas.user import RegisterSchema, LoginSchema, TokenResponse, RefreshSchema
from app.utils.security import hash_password, verify_password
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_token
)
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


def issue_tokens(user, db):
    access_token = create_access_token(user.id, user.role)
    refresh_token, expires_at = create_refresh_token(user.id)

    stored_token = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_token),
        expires_at=expires_at
    )

    db.add(stored_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()

    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role.lower()
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return issue_tokens(user, db)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

    return issue_tokens(user, db)


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshSchema, db: Session = Depends(get_db)):
    try:
        payload = decode_token(data.refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = int(payload["sub"])

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    token_record = db.query(RefreshToken).filter(
        RefreshToken.token_hash == hash_token(data.refresh_token),
        RefreshToken.user_id == user_id,
        RefreshToken.revoked == False
    ).first()

    if not token_record or token_record.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token revoked or expired")

    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive")

    token_record.revoked = True
    db.commit()

    return issue_tokens(user, db)


@router.post("/logout")
def logout(data: RefreshSchema, db: Session = Depends(get_db)):
    token_record = db.query(RefreshToken).filter(
        RefreshToken.token_hash == hash_token(data.refresh_token),
        RefreshToken.revoked == False
    ).first()

    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid or already revoked token")

    token_record.revoked = True
    db.commit()

    return {"message": "Logout successful"}
