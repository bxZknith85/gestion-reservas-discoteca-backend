from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="type_user",
            field=models.ForeignKey(
                blank=True,
                db_column="type_user_id",
                default=None,
                null=True,
                on_delete=models.PROTECT,
                to="catalog.typeuser",
                verbose_name="tipo de usuario",
            ),
        ),
    ]
