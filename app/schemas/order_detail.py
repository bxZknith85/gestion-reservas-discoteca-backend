"""Schemas Pydantic para detalles de orden"""

from decimal import Decimal

from pydantic import BaseModel, Field


class OrderDetailBase(BaseModel):
    order_id: int
    ticket_id: int | None = None
    reservation_id: int | None = None
    type_ticket_id: int | None = None
    table_id: int | None = None
    quantity: int = Field(default=1, gt=0)
    unit_price: Decimal = Field(..., decimal_places=2)
    discount: Decimal = Field(default=0, decimal_places=2, ge=0)


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailUpdate(BaseModel):
    quantity: int | None = None
    unit_price: Decimal | None = None
    discount: Decimal | None = None


class OrderDetailResponse(OrderDetailBase):
    id: int

    class Config:
        from_attributes = True
