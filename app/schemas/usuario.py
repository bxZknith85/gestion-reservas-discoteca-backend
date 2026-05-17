from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    phone_number: str = Field(..., min_length=10)
    type_user_id: int = Field(default=1, description="1=cliente, 2=admin, 3=staff")


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8, description="Contraseña sin encriptar")


class UsuarioUpdate(BaseModel):
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    is_active: bool
    fcm_token: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
