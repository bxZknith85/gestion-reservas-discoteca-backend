"""Schemas Pydantic para tipos de ticket"""

from decimal import Decimal

from pydantic import BaseModel, Field


class TypeTicketBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    event_id: int
    available_quantity: int = Field(..., ge=0)
    max_override: int | None = None
    price: Decimal = Field(..., decimal_places=2)


class TypeTicketCreate(TypeTicketBase):
    pass


class TypeTicketUpdate(BaseModel):
    name: str | None = None
    available_quantity: int | None = None
    max_override: int | None = None
    price: Decimal | None = None


class TypeTicketResponse(TypeTicketBase):
    id: int

    class Config:
        from_attributes = True
