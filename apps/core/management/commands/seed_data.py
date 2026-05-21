from django.core.management.base import BaseCommand

CATALOG_DATA = {
    "TypeUser": [
        (1, "cliente"),
        (2, "admin"),
        (3, "staff"),
    ],
    "EventState": [
        (1, "activo"),
        (2, "cancelado"),
        (3, "finalizado"),
        (4, "borrador"),
    ],
    "ReservationState": [
        (1, "pendiente"),
        (2, "confirmada"),
        (3, "expirada"),
        (4, "cancelada"),
    ],
    "TableState": [
        (1, "disponible"),
        (2, "reservada"),
        (3, "fuera_de_servicio"),
    ],
    "TableType": [
        (1, "regular"),
        (2, "vip"),
        (3, "terraza"),
        (4, "privada"),
    ],
    "TicketState": [
        (1, "activo"),
        (2, "usado"),
        (3, "cancelado"),
    ],
    "PaymentMethod": [
        (1, "efectivo"),
        (2, "transferencia_bancaria"),
        (3, "nequi"),
        (4, "daviplata"),
        (5, "tarjeta_credito"),
        (6, "tarjeta_debito"),
    ],
    "OrderStatus": [
        (1, "pending"),
        (2, "paid"),
        (3, "cancelled"),
        (4, "refunded"),
    ],
}

APPCONFIG_DATA = [
    ("APP_NAME", "Gestión de Reservas - Discoteca"),
    ("MAX_TICKETS_PER_USER", "10"),
    ("RESERVATION_WINDOW_HOURS", "48"),
    ("DEFAULT_CURRENCY", "COP"),
    ("MAINTENANCE_MODE", "false"),
    ("CONTACT_EMAIL", "soporte@discoteca.com"),
]


class Command(BaseCommand):
    help = "Siembra datos iniciales de catálogo y configuración"

    def handle(self, *_args, **_options):
        from django.apps import apps

        for model_name, rows in CATALOG_DATA.items():
            Model = apps.get_model("catalog", model_name)
            for pk, name in rows:
                Model.objects.get_or_create(id=pk, defaults={"name": name})
            self.stdout.write(f"  {model_name}: {len(rows)} registros")

        AppConfig = apps.get_model("system", "AppConfig")
        for key, value in APPCONFIG_DATA:
            AppConfig.objects.get_or_create(key=key, defaults={"value": value})
        self.stdout.write(f"  AppConfig: {len(APPCONFIG_DATA)} registros")
