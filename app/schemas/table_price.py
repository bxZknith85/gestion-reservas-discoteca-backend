"""Schemas Pydantic para precios de mesa"""

from decimal import Decimal

from pydantic import BaseModel, Field


class TablePriceBase(BaseModel):
    table_id: int
    event_id: int
    price: Decimal = Field(..., decimal_places=2, ge=0)


class TablePriceCreate(TablePriceBase):
    pass


class TablePriceUpdate(BaseModel):
    price: Decimal | None = None


class TablePriceResponse(TablePriceBase):
    id: int

    class Config:
        from_attributes = True
