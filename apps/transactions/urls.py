from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.transactions.views import (
    OrderDetailViewSet,
    OrderViewSet,
    PaymentViewSet,
    ReservationViewSet,
    TicketViewSet,
)

router = DefaultRouter()
router.register(r"orders", OrderViewSet)
router.register(r"reservations", ReservationViewSet)
router.register(r"tickets", TicketViewSet)
router.register(r"order-details", OrderDetailViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
