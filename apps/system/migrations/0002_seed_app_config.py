from django.db import migrations


def seed_app_config(apps, schema_editor):
    AppConfig = apps.get_model("system", "AppConfig")
    AppConfig.objects.bulk_create([
        AppConfig(key="APP_NAME", value="Gestión de Reservas - Discoteca"),
        AppConfig(key="MAX_TICKETS_PER_USER", value="10"),
        AppConfig(key="RESERVATION_WINDOW_HOURS", value="48"),
        AppConfig(key="DEFAULT_CURRENCY", value="COP"),
        AppConfig(key="MAINTENANCE_MODE", value="false"),
        AppConfig(key="CONTACT_EMAIL", value="soporte@discoteca.com"),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ("system", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_app_config, migrations.RunPython.noop),
    ]
