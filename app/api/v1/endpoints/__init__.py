from .reservas import router as reservas_router
from .usuarios import router as usuarios_router
from .eventos import router as eventos_router
from .salas import router as salas_router

__all__ = ["reservas_router", "usuarios_router", "eventos_router", "salas_router"]
