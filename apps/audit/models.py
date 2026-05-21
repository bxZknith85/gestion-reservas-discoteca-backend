from django.db import models


class AuditLog(models.Model):
    table_name = models.CharField("tabla", max_length=100)
    record_id = models.IntegerField("ID del registro")
    action = models.CharField(
        "acción",
        max_length=10,
        choices=[("INSERT", "Insert"), ("UPDATE", "Update"), ("DELETE", "Delete")],
    )
    old_data = models.JSONField("datos anteriores", null=True, blank=True)
    new_data = models.JSONField("datos nuevos", null=True, blank=True)
    user = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        db_column="user_id",
        null=True,
        blank=True,
        verbose_name="usuario",
    )
    performed_at = models.DateTimeField("realizado en", auto_now_add=True)

    class Meta:
        db_table = '"audit"."audit_logs"'
        verbose_name = "log de auditoría"
        verbose_name_plural = "logs de auditoría"
        indexes = [
            models.Index(fields=["table_name", "record_id"]),
            models.Index(fields=["performed_at"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.action} on {self.table_name}#{self.record_id} at {self.performed_at}"
