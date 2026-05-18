"""Schemas Pydantic para pagos"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

PAYMENT_STATUSES = {"pending", "confirmed", "rejected", "refunded"}


class PaymentBase(BaseModel):
    order_id: int
    payment_method_id: int
    amount: Decimal = Field(..., decimal_places=2, ge=0)
    status: str = Field(default="pending")
    voucher_url: str | None = None
    reference_number: str | None = None
    notes: str | None = None

    @field_validator("status")
    @classmethod
    def validar_status(cls, v: str) -> str:
        if v not in PAYMENT_STATUSES:
            raise ValueError(f"Status inválido: '{v}'. Permitidos: {', '.join(sorted(PAYMENT_STATUSES))}")
        return v


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: str | None = None
    voucher_url: str | None = None
    reference_number: str | None = None
    confirmed_by: int | None = None
    notes: str | None = None

    @field_validator("status")
    @classmethod
    def validar_status(cls, v: str) -> str:
        if v not in PAYMENT_STATUSES:
            raise ValueError(f"Status inválido: '{v}'. Permitidos: {', '.join(sorted(PAYMENT_STATUSES))}")
        return v


class PaymentResponse(PaymentBase):
    id: int
    confirmed_by: int | None
    confirmed_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True
