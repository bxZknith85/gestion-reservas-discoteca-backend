"""Schemas Pydantic para reservas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReservationBase(BaseModel):
    reservation_state_id: int
    user_id: int
    table_id: int
    event_id: Optional[int] = None
    expires_at: Optional[datetime] = None


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    reservation_state_id: Optional[int] = None
    expires_at: Optional[datetime] = None


class ReservationResponse(ReservationBase):
    id: int
    reserved_at: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
