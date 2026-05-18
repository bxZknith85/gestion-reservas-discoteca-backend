"""Modelos SQLAlchemy - Schema: catalog (Catálogos del sistema)"""

from sqlalchemy import Column, Integer, String

from app.db.database import Base


class TypeUser(Base):
    """Roles de usuario: cliente, admin, staff"""

    __tablename__ = "type_users"
    __table_args__ = {"schema": "catalog"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class EventState(Base):
    """Estados de un evento: activo, cancelado, finalizado"""

    __tablename__ = "event_states"
    __table_args__ = {"schema": "catalog"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class ReservationState(Base):
    """Estados de reserva: pendiente, confirmada, expirada, cancelada"""

    __tablename__ = "reservation_states"
    __table_args__ = {"schema": "catalog"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class TableState(Base):
    """Estados de mesa: disponible, reservada, fuera_de_servicio"""

    __tablename__ = "table_states"
    __table_args__ = {"schema": "catalog"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class TableType(Base):
    """Tipos de mesa: VIP, regular, terraza, etc."""

    __tablename__ = "table_types"
    __table_args__ = {"schema": "catalog"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class TicketState(Base):
    """Estados de ticket: activo, usado, cancelado"""

    __tablename__ = "ticket_states"
    __table_args__ = {"schema": "catalog"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class PaymentMethod(Base):
    """Métodos de pago: efectivo, transferencia, nequi, daviplata, etc."""

    __tablename__ = "payment_methods"
    __table_args__ = {"schema": "catalog"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class OrderStatus(Base):
    """Estados de orden: pending, paid, cancelled, refunded"""

    __tablename__ = "order_statuses"
    __table_args__ = {"schema": "catalog"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
