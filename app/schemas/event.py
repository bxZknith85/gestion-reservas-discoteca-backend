"""Schemas Pydantic para eventos"""

from datetime import datetime

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=300)
    description: str | None = None
    flyer_url: str | None = None
    start_time: datetime
    end_time: datetime
    event_state_id: int | None = None
    created_by: int | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    flyer_url: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    event_state_id: int | None = None


class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
