"""Schemas Pydantic para pagos"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

PAYMENT_STATUSES = {"pending", "confirmed", "rejected", "refunded"}


class PaymentBase(BaseModel):
    order_id: int
    payment_method_id: int
    amount: Decimal = Field(..., decimal_places=2, ge=0)
    status: str = Field(default="pending")
    voucher_url: Optional[str] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validar_status(cls, v: str) -> str:
        if v not in PAYMENT_STATUSES:
            raise ValueError(f"Status inválido: '{v}'. Permitidos: {', '.join(sorted(PAYMENT_STATUSES))}")
        return v


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    voucher_url: Optional[str] = None
    reference_number: Optional[str] = None
    confirmed_by: Optional[int] = None
    notes: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validar_status(cls, v: str) -> str:
        if v not in PAYMENT_STATUSES:
            raise ValueError(f"Status inválido: '{v}'. Permitidos: {', '.join(sorted(PAYMENT_STATUSES))}")
        return v


class PaymentResponse(PaymentBase):
    id: int
    confirmed_by: Optional[int]
    confirmed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
