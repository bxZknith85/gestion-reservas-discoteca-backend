"""Schemas Pydantic para tipos de ticket"""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class TypeTicketBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    event_id: int
    available_quantity: int = Field(..., ge=0)
    max_override: Optional[int] = None
    price: Decimal = Field(..., decimal_places=2)


class TypeTicketCreate(TypeTicketBase):
    pass


class TypeTicketUpdate(BaseModel):
    name: Optional[str] = None
    available_quantity: Optional[int] = None
    max_override: Optional[int] = None
    price: Optional[Decimal] = None


class TypeTicketResponse(TypeTicketBase):
    id: int
    
    class Config:
        from_attributes = True
