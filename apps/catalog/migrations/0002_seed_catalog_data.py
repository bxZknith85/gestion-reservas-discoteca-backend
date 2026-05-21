from django.db import migrations


def seed_catalog_data(apps, schema_editor):
    TypeUser = apps.get_model("catalog", "TypeUser")
    TypeUser.objects.bulk_create([
        TypeUser(id=1, name="cliente"),
        TypeUser(id=2, name="admin"),
        TypeUser(id=3, name="staff"),
    ])

    EventState = apps.get_model("catalog", "EventState")
    EventState.objects.bulk_create([
        EventState(id=1, name="activo"),
        EventState(id=2, name="cancelado"),
        EventState(id=3, name="finalizado"),
        EventState(id=4, name="borrador"),
    ])

    ReservationState = apps.get_model("catalog", "ReservationState")
    ReservationState.objects.bulk_create([
        ReservationState(id=1, name="pendiente"),
        ReservationState(id=2, name="confirmada"),
        ReservationState(id=3, name="expirada"),
        ReservationState(id=4, name="cancelada"),
    ])

    TableState = apps.get_model("catalog", "TableState")
    TableState.objects.bulk_create([
        TableState(id=1, name="disponible"),
        TableState(id=2, name="reservada"),
        TableState(id=3, name="fuera_de_servicio"),
    ])

    TableType = apps.get_model("catalog", "TableType")
    TableType.objects.bulk_create([
        TableType(id=1, name="regular"),
        TableType(id=2, name="vip"),
        TableType(id=3, name="terraza"),
        TableType(id=4, name="privada"),
    ])

    TicketState = apps.get_model("catalog", "TicketState")
    TicketState.objects.bulk_create([
        TicketState(id=1, name="activo"),
        TicketState(id=2, name="usado"),
        TicketState(id=3, name="cancelado"),
    ])

    PaymentMethod = apps.get_model("catalog", "PaymentMethod")
    PaymentMethod.objects.bulk_create([
        PaymentMethod(id=1, name="efectivo"),
        PaymentMethod(id=2, name="transferencia_bancaria"),
        PaymentMethod(id=3, name="nequi"),
        PaymentMethod(id=4, name="daviplata"),
        PaymentMethod(id=5, name="tarjeta_credito"),
        PaymentMethod(id=6, name="tarjeta_debito"),
    ])

    OrderStatus = apps.get_model("catalog", "OrderStatus")
    OrderStatus.objects.bulk_create([
        OrderStatus(id=1, name="pending"),
        OrderStatus(id=2, name="paid"),
        OrderStatus(id=3, name="cancelled"),
        OrderStatus(id=4, name="refunded"),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_catalog_data, migrations.RunPython.noop),
    ]
