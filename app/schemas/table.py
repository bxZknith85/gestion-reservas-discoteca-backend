"""Schemas Pydantic para mesas"""

from pydantic import BaseModel, Field


class DicoTableBase(BaseModel):
    number: int = Field(..., gt=0)
    table_type_id: int
    capacity: int = Field(..., gt=0)
    table_state_id: int


class DicoTableCreate(DicoTableBase):
    pass


class DicoTableUpdate(BaseModel):
    number: int | None = None
    table_type_id: int | None = None
    capacity: int | None = None
    table_state_id: int | None = None


class DicoTableResponse(DicoTableBase):
    id: int

    class Config:
        from_attributes = True
