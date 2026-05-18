"""Schemas Pydantic para tickets"""

from datetime import datetime

from pydantic import BaseModel


class TicketBase(BaseModel):
    user_id: int
    type_ticket_id: int
    ticket_state_id: int


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    ticket_state_id: int | None = None


class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
