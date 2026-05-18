from .events import router as events_router
from .order_details import router as order_details_router
from .orders import router as orders_router
from .reservations import router as reservations_router
from .table_prices import router as table_prices_router
from .tables import router as tables_router
from .tickets import router as tickets_router
from .type_tickets import router as type_tickets_router
from .users import router as users_router

__all__ = [
    "users_router",
    "events_router",
    "tables_router",
    "type_tickets_router",
    "table_prices_router",
    "reservations_router",
    "tickets_router",
    "orders_router",
    "order_details_router",
]
