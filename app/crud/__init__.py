from .usuario import CRUDUsuario
from .event import CRUDEvent
from .dico_table import CRUDDicoTable
from .reservation import CRUDReservation

usuario = CRUDUsuario()
event = CRUDEvent()
table = CRUDDicoTable()
reservation = CRUDReservation()

__all__ = ["usuario", "event", "table", "reservation"]
