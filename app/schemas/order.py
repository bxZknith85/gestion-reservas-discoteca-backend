"""Schemas Pydantic para órdenes"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

ORDER_STATUSES = {"pending", "paid", "cancelled", "refunded"}


class OrderBase(BaseModel):
    user_id: int
    status: str = Field(default="pending")
    notes: str | None = None

    @field_validator("status")
    @classmethod
    def validar_status(cls, v: str) -> str:
        if v not in ORDER_STATUSES:
            raise ValueError(f"Status inválido: '{v}'. Permitidos: {', '.join(sorted(ORDER_STATUSES))}")
        return v


class OrderCreate(OrderBase):
    total: Decimal = Field(default=0, decimal_places=2)


class OrderUpdate(BaseModel):
    status: str | None = None
    total: Decimal | None = None
    notes: str | None = None

    @field_validator("status")
    @classmethod
    def validar_status(cls, v: str) -> str:
        if v not in ORDER_STATUSES:
            raise ValueError(f"Status inválido: '{v}'. Permitidos: {', '.join(sorted(ORDER_STATUSES))}")
        return v


class OrderResponse(OrderBase):
    id: int
    ordered_at: datetime
    total: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
