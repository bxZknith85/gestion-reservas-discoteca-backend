from .users import router as users_router
from .events import router as events_router
from .tables import router as tables_router
from .reservations import router as reservations_router
from .tickets import router as tickets_router
from .orders import router as orders_router

__all__ = [
    "users_router",
    "events_router",
    "tables_router",
    "reservations_router",
    "tickets_router",
    "orders_router",
]
