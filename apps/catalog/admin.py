from django.contrib import admin

from apps.catalog.models import (
    EventState,
    OrderStatus,
    PaymentMethod,
    ReservationState,
    TableState,
    TableType,
    TicketState,
    TypeUser,
)

admin.site.register(TypeUser)
admin.site.register(EventState)
admin.site.register(ReservationState)
admin.site.register(TableState)
admin.site.register(TableType)
admin.site.register(TicketState)
admin.site.register(PaymentMethod)
admin.site.register(OrderStatus)
