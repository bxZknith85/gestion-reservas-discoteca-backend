"""Modelos SQLAlchemy - Schema: core (Entidades principales)"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Numeric, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.db.database import Base


class User(Base):
    """Tabla de usuarios del sistema"""
    __tablename__ = "users"
    __table_args__ = (
        {"schema": "core"},
    )
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(50), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    type_user_id = Column(Integer, ForeignKey("catalog.type_users.id"), nullable=False)
    fcm_token = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    events = relationship("Event", back_populates="created_by_user", foreign_keys="Event.created_by")
    reservations = relationship("Reservation", back_populates="user")
    tickets = relationship("Ticket", back_populates="user")
    orders = relationship("Order", back_populates="user")
    payments_confirmed = relationship("Payment", back_populates="confirmed_by_user", foreign_keys="Payment.confirmed_by")
    admin_actions = relationship("AdminActionLog", back_populates="admin")


class Event(Base):
    """Tabla de eventos"""
    __tablename__ = "events"
    __table_args__ = (
        {"schema": "core"},
    )
    
    id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    flyer_url = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    event_state_id = Column(Integer, ForeignKey("catalog.event_states.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("core.users.id"), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    created_by_user = relationship("User", back_populates="events", foreign_keys=[created_by])
    type_tickets = relationship("TypeTicket", back_populates="event")
    table_prices = relationship("TablePrice", back_populates="event")
    reservations = relationship("Reservation", back_populates="event")


class DicoTable(Base):
    """Tabla de mesas físicas de la discoteca"""
    __tablename__ = "dico_tables"
    __table_args__ = (
        {"schema": "core"},
    )
    
    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True, nullable=False)
    table_type_id = Column(Integer, ForeignKey("catalog.table_types.id"), nullable=False)
    capacity = Column(Integer, nullable=False)
    table_state_id = Column(Integer, ForeignKey("catalog.table_states.id"), nullable=False)
    
    # Relaciones
    table_prices = relationship("TablePrice", back_populates="table")
    reservations = relationship("Reservation", back_populates="table")


class TypeTicket(Base):
    """Tipos de entrada por evento"""
    __tablename__ = "type_tickets"
    __table_args__ = (
        {"schema": "core"},
    )
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    event_id = Column(Integer, ForeignKey("core.events.id"), nullable=False)
    available_quantity = Column(Integer, nullable=False)
    max_override = Column(Integer, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    
    # Relaciones
    event = relationship("Event", back_populates="type_tickets")
    tickets = relationship("Ticket", back_populates="type_ticket")


class TablePrice(Base):
    """Precio de reserva de cada mesa según el evento"""
    __tablename__ = "table_prices"
    __table_args__ = (
        {"schema": "core"},
    )
    
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey("core.dico_tables.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("core.events.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    
    # Relaciones
    table = relationship("DicoTable", back_populates="table_prices")
    event = relationship("Event", back_populates="table_prices")
