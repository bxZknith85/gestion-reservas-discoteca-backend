"""Modelos SQLAlchemy - Schema: transactions (Flujo de compra)"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.db.database import Base


class Order(Base):
    """Tabla de órdenes/pedidos"""
    __tablename__ = "orders"
    __table_args__ = (
        {"schema": "transactions"},
    )
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id"), nullable=False)
    ordered_at = Column(DateTime, default=func.now(), nullable=False)
    total = Column(Numeric(10, 2), default=0, nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    payments = relationship("Payment", back_populates="order")


class Reservation(Base):
    """Tabla de reservas"""
    __tablename__ = "reservations"
    __table_args__ = (
        {"schema": "transactions"},
    )
    
    id = Column(Integer, primary_key=True)
    reservation_state_id = Column(Integer, ForeignKey("catalog.reservation_states.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("core.users.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("core.dico_tables.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("core.events.id"), nullable=True)
    reserved_at = Column(DateTime, default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="reservations")
    table = relationship("DicoTable", back_populates="reservations")
    event = relationship("Event", back_populates="reservations")
    order_details = relationship("OrderDetail", back_populates="reservation")


class Ticket(Base):
    """Tabla de tickets/entradas compradas"""
    __tablename__ = "tickets"
    __table_args__ = (
        {"schema": "transactions"},
    )
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id"), nullable=False)
    type_ticket_id = Column(Integer, ForeignKey("core.type_tickets.id"), nullable=False)
    ticket_state_id = Column(Integer, ForeignKey("catalog.ticket_states.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="tickets")
    type_ticket = relationship("TypeTicket", back_populates="tickets")
    order_details = relationship("OrderDetail", back_populates="ticket")


class OrderDetail(Base):
    """Detalles de cada orden (tickets y/o reservas)"""
    __tablename__ = "order_details"
    __table_args__ = (
        {"schema": "transactions"},
    )
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("transactions.orders.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("transactions.tickets.id"), nullable=True)
    reservation_id = Column(Integer, ForeignKey("transactions.reservations.id"), nullable=True)
    type_ticket_id = Column(Integer, ForeignKey("core.type_tickets.id"), nullable=True)
    table_id = Column(Integer, ForeignKey("core.dico_tables.id"), nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Relaciones
    order = relationship("Order", back_populates="order_details")
    ticket = relationship("Ticket", back_populates="order_details")
    reservation = relationship("Reservation", back_populates="order_details")


class Payment(Base):
    """Tabla de pagos"""
    __tablename__ = "payments"
    __table_args__ = (
        {"schema": "transactions"},
    )
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("transactions.orders.id"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("catalog.payment_methods.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    voucher_url = Column(Text, nullable=True)
    reference_number = Column(Text, nullable=True)
    confirmed_by = Column(Integer, ForeignKey("core.users.id"), nullable=True)
    confirmed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relaciones
    order = relationship("Order", back_populates="payments")
    confirmed_by_user = relationship("User", back_populates="payments_confirmed", foreign_keys=[confirmed_by])
