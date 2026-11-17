from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UpdateUserSchema, StatusSchema, RoleSchema
from app.dependencies.auth import get_current_user, require_roles

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin"))
):
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UpdateUserSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    duplicate = db.query(User).filter(
        User.email == data.email,
        User.id != user_id
    ).first()

    if duplicate:
        raise HTTPException(status_code=409, detail="Email already registered")

    user.name = data.name
    user.email = data.email

    db.commit()
    db.refresh(user)

    return user


@router.patch("/{user_id}/status", response_model=UserResponse)
def update_status(
    user_id: int,
    data: StatusSchema,
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin"))
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id and not data.is_active:
        raise HTTPException(status_code=400, detail="Admin cannot deactivate own account")

    user.is_active = data.is_active
    db.commit()
    db.refresh(user)

    return user


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_role(
    user_id: int,
    data: RoleSchema,
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin"))
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = data.role
    db.commit()
    db.refresh(user)

    return user
