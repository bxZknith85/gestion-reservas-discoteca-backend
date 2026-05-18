from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class EstadoReserva(str, Enum):
    """Enumeración para estados de reserva"""

    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    COMPLETADA = "completada"


class RolUsuario(str, Enum):
    """Enumeración para roles de usuario"""

    ADMIN = "admin"
    CLIENTE = "cliente"
    GERENTE = "gerente"


class Sala(Base):
    """Modelo de Sala"""

    __tablename__ = "salas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    capacidad_maxima = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=True)
    ubicacion = Column(String(255), nullable=True)
    activa = Column(Boolean, default=True, index=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    eventos = relationship("Evento", back_populates="sala")
    reservas = relationship("Reserva", back_populates="sala")


class Evento(Base):
    """Modelo de Evento"""

    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    sala_id = Column(Integer, ForeignKey("salas.id"), nullable=False)
    fecha_inicio = Column(DateTime(timezone=True), nullable=False)
    fecha_fin = Column(DateTime(timezone=True), nullable=False)
    precio_entrada = Column(Float, default=0.0, nullable=False)
    capacidad_disponible = Column(Integer, nullable=False)
    activo = Column(Boolean, default=True, index=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    sala = relationship("Sala", back_populates="eventos")
    reservas = relationship("Reserva", back_populates="evento")


class Reserva(Base):
    """Modelo de Reserva"""

    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    sala_id = Column(Integer, ForeignKey("salas.id"), nullable=False)
    numero_personas = Column(Integer, nullable=False)
    estado = Column(SQLEnum(EstadoReserva), default=EstadoReserva.PENDIENTE, nullable=False)
    fecha_reserva = Column(DateTime(timezone=True), nullable=False)
    notas = Column(Text, nullable=True)
    monto_total = Column(Float, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="reservas")
    evento = relationship("Evento", back_populates="reservas")
    sala = relationship("Sala", back_populates="reservas")
