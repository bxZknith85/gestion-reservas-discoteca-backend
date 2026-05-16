"""Schemas Pydantic para pagos"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class PaymentBase(BaseModel):
    order_id: int
    payment_method_id: int
    amount: Decimal = Field(..., decimal_places=2, ge=0)
    status: str = Field(default="pending")
    voucher_url: Optional[str] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    voucher_url: Optional[str] = None
    reference_number: Optional[str] = None
    confirmed_by: Optional[int] = None
    notes: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: int
    confirmed_by: Optional[int]
    confirmed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
