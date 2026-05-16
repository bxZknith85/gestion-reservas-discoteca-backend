"""Schemas Pydantic para órdenes"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class OrderBase(BaseModel):
    user_id: int
    status: str = Field(default="pending")
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    total: Decimal = Field(default=0, decimal_places=2)


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    total: Optional[Decimal] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    ordered_at: datetime
    total: Decimal
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
