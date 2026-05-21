from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def root_view(_request):
    return Response({
        "status": "ok",
        "service": "Gestión de Reservas - Discoteca",
    })


api_prefix = settings.API_V1_STR.lstrip("/")

urlpatterns = [
    path("", root_view, name="root"),
    path("admin/", admin.site.urls),
    path(f"{api_prefix}/", include("apps.core.urls")),
    path(f"{api_prefix}/", include("apps.transactions.urls")),
    path(f"{api_prefix}/", include("apps.catalog.urls")),
    path(f"{api_prefix}/", include("apps.audit.urls")),
    path(f"{api_prefix}/", include("apps.system.urls")),
    path("health/", include("apps.core.urls_health")),
    path(f"{api_prefix}/health/", include("apps.core.urls_health")),
]
