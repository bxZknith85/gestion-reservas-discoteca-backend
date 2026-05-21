from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.core.auth import login_view
from apps.core.views import (
    DicoTableViewSet,
    EventViewSet,
    TablePriceViewSet,
    TypeTicketViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"events", EventViewSet)
router.register(r"tables", DicoTableViewSet)
router.register(r"type-tickets", TypeTicketViewSet)
router.register(r"table-prices", TablePriceViewSet)

urlpatterns = [
    path("auth/login/", login_view, name="auth-login"),
    path("", include(router.urls)),
]
