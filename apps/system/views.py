from rest_framework import viewsets

from apps.system.models import AdminActionLog, AppConfig
from apps.system.serializers import AdminActionLogSerializer, AppConfigSerializer


class AdminActionLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdminActionLog.objects.all()
    serializer_class = AdminActionLogSerializer


class AppConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer
