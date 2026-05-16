# Importar todos los modelos de los diferentes schemas
from app.models.catalog import (
    TypeUser, EventState, ReservationState, TableState, 
    TableType, TicketState, PaymentMethod, OrderStatus
)
from app.models.core import User, Event, DicoTable, TypeTicket, TablePrice
from app.models.transactions import Order, Reservation, Ticket, OrderDetail, Payment
from app.models.audit import AuditLog
from app.models.system import AdminActionLog, AppConfig

__all__ = [
    # Catalog
    "TypeUser", "EventState", "ReservationState", "TableState",
    "TableType", "TicketState", "PaymentMethod", "OrderStatus",
    # Core
    "User", "Event", "DicoTable", "TypeTicket", "TablePrice",
    # Transactions
    "Order", "Reservation", "Ticket", "OrderDetail", "Payment",
    # Audit
    "AuditLog",
    # System
    "AdminActionLog", "AppConfig",
]
