from datetime import datetime

from pydantic import BaseModel, Field


class SalaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    capacidad_maxima: int = Field(..., gt=0)
    descripcion: str | None = None
    ubicacion: str | None = None


class SalaCreate(SalaBase):
    pass


class SalaUpdate(BaseModel):
    nombre: str | None = None
    capacidad_maxima: int | None = None
    descripcion: str | None = None
    ubicacion: str | None = None


class SalaResponse(SalaBase):
    id: int
    activa: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True
