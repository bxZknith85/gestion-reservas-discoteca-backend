"""Schemas Pydantic para usuarios"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    phone_number: str = Field(..., min_length=7, max_length=50)
    type_user_id: int
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    fcm_token: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    fcm_token: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
