from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReservaBase(BaseModel):
    usuario_id: int
    evento_id: int
    sala_id: int
    numero_personas: int = Field(..., gt=0)
    fecha_reserva: datetime
    notas: Optional[str] = None


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(BaseModel):
    numero_personas: Optional[int] = None
    estado: Optional[str] = None
    notas: Optional[str] = None


class ReservaResponse(ReservaBase):
    id: int
    estado: str
    monto_total: Optional[float]
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True
