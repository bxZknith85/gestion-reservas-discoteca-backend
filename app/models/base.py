# Importar todos los modelos de los diferentes schemas
from app.models.audit import AuditLog
from app.models.catalog import (
    EventState,
    OrderStatus,
    PaymentMethod,
    ReservationState,
    TableState,
    TableType,
    TicketState,
    TypeUser,
)
from app.models.core import DicoTable, Event, TablePrice, TypeTicket, User
from app.models.system import AdminActionLog, AppConfig
from app.models.transactions import Order, OrderDetail, Payment, Reservation, Ticket

__all__ = [
    # Catalog
    "TypeUser",
    "EventState",
    "ReservationState",
    "TableState",
    "TableType",
    "TicketState",
    "PaymentMethod",
    "OrderStatus",
    # Core
    "User",
    "Event",
    "DicoTable",
    "TypeTicket",
    "TablePrice",
    # Transactions
    "Order",
    "Reservation",
    "Ticket",
    "OrderDetail",
    "Payment",
    # Audit
    "AuditLog",
    # System
    "AdminActionLog",
    "AppConfig",
]
