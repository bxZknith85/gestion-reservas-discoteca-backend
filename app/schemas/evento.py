from datetime import datetime

from pydantic import BaseModel, Field


class EventoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    descripcion: str | None = None
    sala_id: int
    fecha_inicio: datetime
    fecha_fin: datetime
    precio_entrada: float = Field(..., ge=0)
    capacidad_disponible: int = Field(..., gt=0)


class EventoCreate(EventoBase):
    pass


class EventoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    precio_entrada: float | None = None
    capacidad_disponible: int | None = None


class EventoResponse(EventoBase):
    id: int
    activo: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True
