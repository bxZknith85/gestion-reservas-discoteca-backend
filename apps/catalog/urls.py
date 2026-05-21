from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.catalog.views import (
    EventStateViewSet,
    OrderStatusViewSet,
    PaymentMethodViewSet,
    ReservationStateViewSet,
    TableStateViewSet,
    TableTypeViewSet,
    TicketStateViewSet,
    TypeUserViewSet,
)

router = DefaultRouter()
router.register(r"type-users", TypeUserViewSet)
router.register(r"event-states", EventStateViewSet)
router.register(r"reservation-states", ReservationStateViewSet)
router.register(r"table-states", TableStateViewSet)
router.register(r"table-types", TableTypeViewSet)
router.register(r"ticket-states", TicketStateViewSet)
router.register(r"payment-methods", PaymentMethodViewSet)
router.register(r"order-statuses", OrderStatusViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
