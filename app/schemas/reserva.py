from datetime import datetime

from pydantic import BaseModel, Field


class ReservaBase(BaseModel):
    usuario_id: int
    evento_id: int
    sala_id: int
    numero_personas: int = Field(..., gt=0)
    fecha_reserva: datetime
    notas: str | None = None


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(BaseModel):
    numero_personas: int | None = None
    estado: str | None = None
    notas: str | None = None


class ReservaResponse(ReservaBase):
    id: int
    estado: str
    monto_total: float | None
    fecha_creacion: datetime

    class Config:
        from_attributes = True
