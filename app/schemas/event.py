"""Schemas Pydantic para eventos"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=300)
    description: Optional[str] = None
    flyer_url: Optional[str] = None
    start_time: datetime
    end_time: datetime
    event_state_id: Optional[int] = None
    created_by: Optional[int] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    flyer_url: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    event_state_id: Optional[int] = None


class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
