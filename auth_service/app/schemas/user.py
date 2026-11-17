from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal
from datetime import datetime


class RegisterSchema(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Literal["vendor", "customer"] = "customer"


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshSchema(BaseModel):
    refresh_token: str


class UpdateUserSchema(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class StatusSchema(BaseModel):
    is_active: bool


class RoleSchema(BaseModel):
    role: Literal["admin", "vendor", "customer"]
