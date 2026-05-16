from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EventoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: Optional[str] = None
    sala_id: int
    fecha_inicio: datetime
    fecha_fin: datetime
    precio_entrada: float = Field(..., ge=0)
    capacidad_disponible: int = Field(..., gt=0)


class EventoCreate(EventoBase):
    pass


class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    precio_entrada: Optional[float] = None
    capacidad_disponible: Optional[int] = None


class EventoResponse(EventoBase):
    id: int
    activo: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True
