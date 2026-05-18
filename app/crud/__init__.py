from .dico_table import CRUDDicoTable
from .event import CRUDEvent
from .order import CRUDOrder
from .order_detail import CRUDOrderDetail
from .payment import CRUDPayment
from .reservation import CRUDReservation
from .table_price import CRUDTablePrice
from .ticket import CRUDTicket
from .type_ticket import CRUDTypeTicket
from .usuario import CRUDUsuario

usuario = CRUDUsuario()
event = CRUDEvent()
table = CRUDDicoTable()
type_ticket = CRUDTypeTicket()
table_price = CRUDTablePrice()
reservation = CRUDReservation()
ticket = CRUDTicket()
order = CRUDOrder()
order_detail = CRUDOrderDetail()
payment = CRUDPayment()

__all__ = [
    "usuario",
    "event",
    "table",
    "type_ticket",
    "table_price",
    "reservation",
    "ticket",
    "order",
    "order_detail",
    "payment",
]
