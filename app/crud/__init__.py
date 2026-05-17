from .usuario import CRUDUsuario
from .event import CRUDEvent
from .dico_table import CRUDDicoTable
from .reservation import CRUDReservation
from .ticket import CRUDTicket

usuario = CRUDUsuario()
event = CRUDEvent()
table = CRUDDicoTable()
reservation = CRUDReservation()
ticket = CRUDTicket()

__all__ = ["usuario", "event", "table", "reservation", "ticket"]
