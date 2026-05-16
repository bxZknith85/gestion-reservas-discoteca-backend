from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SalaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    capacidad_maxima: int = Field(..., gt=0)
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None


class SalaCreate(SalaBase):
    pass


class SalaUpdate(BaseModel):
    nombre: Optional[str] = None
    capacidad_maxima: Optional[int] = None
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None


class SalaResponse(SalaBase):
    id: int
    activa: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True
