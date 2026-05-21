from django.conf import settings
from django.contrib import admin
from django.urls import include, path

api_prefix = settings.API_V1_STR.lstrip("/")

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{api_prefix}/", include("apps.core.urls")),
    path(f"{api_prefix}/", include("apps.transactions.urls")),
    path(f"{api_prefix}/", include("apps.catalog.urls")),
    path(f"{api_prefix}/", include("apps.audit.urls")),
    path(f"{api_prefix}/", include("apps.system.urls")),
    path("health/", include("apps.core.urls_health")),
    path(f"{api_prefix}/health/", include("apps.core.urls_health")),
]
