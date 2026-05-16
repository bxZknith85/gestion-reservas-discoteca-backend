"""Schemas Pydantic para mesas"""
from pydantic import BaseModel, Field
from typing import Optional


class DicoTableBase(BaseModel):
    number: int = Field(..., gt=0)
    table_type_id: int
    capacity: int = Field(..., gt=0)
    table_state_id: int


class DicoTableCreate(DicoTableBase):
    pass


class DicoTableUpdate(BaseModel):
    number: Optional[int] = None
    table_type_id: Optional[int] = None
    capacity: Optional[int] = None
    table_state_id: Optional[int] = None


class DicoTableResponse(DicoTableBase):
    id: int
    
    class Config:
        from_attributes = True
