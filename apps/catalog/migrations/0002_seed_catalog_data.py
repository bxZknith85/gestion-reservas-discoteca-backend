from django.db import migrations


def _seed(apps, model_name, rows):
    Model = apps.get_model("catalog", model_name)
    for row in rows:
        Model.objects.get_or_create(id=row["id"], defaults={"name": row["name"]})


def seed_catalog_data(apps, schema_editor):
    _seed(apps, "TypeUser", [
        {"id": 1, "name": "cliente"},
        {"id": 2, "name": "admin"},
        {"id": 3, "name": "staff"},
    ])
    _seed(apps, "EventState", [
        {"id": 1, "name": "activo"},
        {"id": 2, "name": "cancelado"},
        {"id": 3, "name": "finalizado"},
        {"id": 4, "name": "borrador"},
    ])
    _seed(apps, "ReservationState", [
        {"id": 1, "name": "pendiente"},
        {"id": 2, "name": "confirmada"},
        {"id": 3, "name": "expirada"},
        {"id": 4, "name": "cancelada"},
    ])
    _seed(apps, "TableState", [
        {"id": 1, "name": "disponible"},
        {"id": 2, "name": "reservada"},
        {"id": 3, "name": "fuera_de_servicio"},
    ])
    _seed(apps, "TableType", [
        {"id": 1, "name": "regular"},
        {"id": 2, "name": "vip"},
        {"id": 3, "name": "terraza"},
        {"id": 4, "name": "privada"},
    ])
    _seed(apps, "TicketState", [
        {"id": 1, "name": "activo"},
        {"id": 2, "name": "usado"},
        {"id": 3, "name": "cancelado"},
    ])
    _seed(apps, "PaymentMethod", [
        {"id": 1, "name": "efectivo"},
        {"id": 2, "name": "transferencia_bancaria"},
        {"id": 3, "name": "nequi"},
        {"id": 4, "name": "daviplata"},
        {"id": 5, "name": "tarjeta_credito"},
        {"id": 6, "name": "tarjeta_debito"},
    ])
    _seed(apps, "OrderStatus", [
        {"id": 1, "name": "pending"},
        {"id": 2, "name": "paid"},
        {"id": 3, "name": "cancelled"},
        {"id": 4, "name": "refunded"},
    ])


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_catalog_data, migrations.RunPython.noop),
    ]
