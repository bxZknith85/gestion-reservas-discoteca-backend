from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.system.views import AdminActionLogViewSet, AppConfigViewSet

router = DefaultRouter()
router.register(r"admin-actions", AdminActionLogViewSet)
router.register(r"app-config", AppConfigViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
