"""Schemas Pydantic para precios de mesa"""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class TablePriceBase(BaseModel):
    table_id: int
    event_id: int
    price: Decimal = Field(..., decimal_places=2, ge=0)


class TablePriceCreate(TablePriceBase):
    pass


class TablePriceUpdate(BaseModel):
    price: Optional[Decimal] = None


class TablePriceResponse(TablePriceBase):
    id: int
    
    class Config:
        from_attributes = True
