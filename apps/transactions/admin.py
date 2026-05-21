from django.contrib import admin

from apps.transactions.models import (
    Order,
    OrderDetail,
    Payment,
    Reservation,
    Ticket,
)

admin.site.register(Order)
admin.site.register(Reservation)
admin.site.register(Ticket)
admin.site.register(OrderDetail)
admin.site.register(Payment)
