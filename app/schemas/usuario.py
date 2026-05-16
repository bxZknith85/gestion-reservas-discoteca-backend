from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    nombre_completo: str = Field(..., min_length=3, max_length=255)
    numero_telefono: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8)


class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    numero_telefono: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    id: int
    rol: str
    activo: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True
