from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.core.auth import (
    change_password_view,
    login_view,
    token_refresh_view,
    token_verify_view,
)
from apps.core.views import (
    DicoTableViewSet,
    EventViewSet,
    TablePriceViewSet,
    TypeTicketViewSet,
    UserViewSet,
    dashboard_stats_view,
    reservation_availability_view,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"events", EventViewSet)
router.register(r"tables", DicoTableViewSet)
router.register(r"type-tickets", TypeTicketViewSet)
router.register(r"table-prices", TablePriceViewSet)

urlpatterns = [
    path("auth/login/", login_view, name="auth-login"),
    path("auth/refresh/", token_refresh_view, name="auth-refresh"),
    path("auth/verify/", token_verify_view, name="auth-verify"),
    path("auth/change-password/", change_password_view, name="auth-change-password"),
    path("reservations/availability/", reservation_availability_view, name="reservation-availability"),
    path("dashboard/stats/", dashboard_stats_view, name="dashboard-stats"),
    path("", include(router.urls)),
]
