"""Schemas Pydantic para detalles de orden"""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class OrderDetailBase(BaseModel):
    order_id: int
    ticket_id: Optional[int] = None
    reservation_id: Optional[int] = None
    type_ticket_id: Optional[int] = None
    table_id: Optional[int] = None
    quantity: int = Field(default=1, gt=0)
    unit_price: Decimal = Field(..., decimal_places=2)
    discount: Decimal = Field(default=0, decimal_places=2, ge=0)


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailUpdate(BaseModel):
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None
    discount: Optional[Decimal] = None


class OrderDetailResponse(OrderDetailBase):
    id: int
    
    class Config:
        from_attributes = True
