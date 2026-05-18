"""Schemas Pydantic para usuarios"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    phone_number: str = Field(..., min_length=7, max_length=50)
    type_user_id: int
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    fcm_token: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    fcm_token: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
