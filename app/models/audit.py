"""Modelos SQLAlchemy - Schema: audit (Auditoría)"""

from sqlalchemy import JSON, BigInteger, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.database import Base


class AuditLog(Base):
    """Tabla de auditoría para trazabilidad de cambios"""

    __tablename__ = "audit_logs"
    __table_args__ = ({"schema": "audit"},)

    id = Column(BigInteger, primary_key=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String(10), nullable=False)  # INSERT, UPDATE, DELETE
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    user_id = Column(Integer, nullable=True)
    performed_at = Column(DateTime, default=func.now(), nullable=False)
