"""Modelos SQLAlchemy - Schema: system (Sistema)"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class AdminActionLog(Base):
    """Tabla de registro de acciones administrativas"""
    __tablename__ = "admin_actions_log"
    __table_args__ = (
        {"schema": "system"},
    )
    
    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey("core.users.id"), nullable=False)
    action = Column(Text, nullable=False)
    payload = Column(JSON, nullable=True)
    ip_address = Column(Text, nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relaciones
    admin = relationship("User", back_populates="admin_actions")


class AppConfig(Base):
    """Tabla de configuración global de la aplicación"""
    __tablename__ = "app_config"
    __table_args__ = (
        {"schema": "system"},
    )
    
    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
