from django.db import models


class AdminActionLog(models.Model):
    admin = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        db_column="admin_id",
        verbose_name="admin",
    )
    action = models.TextField("acción")
    payload = models.JSONField("datos", null=True, blank=True)
    ip_address = models.TextField("dirección IP", null=True, blank=True)
    user_agent = models.TextField("user agent", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"system"."admin_actions_log"'
        verbose_name = "acción de administrador"
        verbose_name_plural = "acciones de administradores"
        indexes = [
            models.Index(fields=["admin"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.admin.username} - {self.action[:50]}"


class AppConfig(models.Model):
    key = models.CharField("clave", max_length=100, primary_key=True)
    value = models.TextField("valor")
    description = models.TextField("descripción", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"system"."app_config"'
        verbose_name = "configuración"
        verbose_name_plural = "configuraciones"

    def __str__(self):
        return f"{self.key}={self.value}"
