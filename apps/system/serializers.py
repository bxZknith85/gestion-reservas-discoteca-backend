from rest_framework import serializers

from apps.system.models import AdminActionLog, AppConfig


class AdminActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminActionLog
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        fields = "__all__"
