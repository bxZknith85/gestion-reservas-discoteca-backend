from .usuario import CRUDUsuario
from .reserva import CRUDReserva
from .evento import CRUDEvento
from .sala import CRUDSala

usuario = CRUDUsuario()
reserva = CRUDReserva()
evento = CRUDEvento()
sala = CRUDSala()

__all__ = ["usuario", "reserva", "evento", "sala"]
