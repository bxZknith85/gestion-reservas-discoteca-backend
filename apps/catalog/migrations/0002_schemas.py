from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "CREATE SCHEMA IF NOT EXISTS catalog",
                "CREATE SCHEMA IF NOT EXISTS core",
                "CREATE SCHEMA IF NOT EXISTS transactions",
                "CREATE SCHEMA IF NOT EXISTS audit",
                "CREATE SCHEMA IF NOT EXISTS system",
            ],
            reverse_sql=[
                "DROP SCHEMA IF EXISTS system CASCADE",
                "DROP SCHEMA IF EXISTS audit CASCADE",
                "DROP SCHEMA IF EXISTS transactions CASCADE",
                "DROP SCHEMA IF EXISTS core CASCADE",
                "DROP SCHEMA IF EXISTS catalog CASCADE",
            ],
        ),
    ]
