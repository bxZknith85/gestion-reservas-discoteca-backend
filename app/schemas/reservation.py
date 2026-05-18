"""Schemas Pydantic para reservas"""

from datetime import datetime

from pydantic import BaseModel


class ReservationBase(BaseModel):
    reservation_state_id: int
    user_id: int
    table_id: int
    event_id: int | None = None
    expires_at: datetime | None = None


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    reservation_state_id: int | None = None
    expires_at: datetime | None = None


class ReservationResponse(ReservationBase):
    id: int
    reserved_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
