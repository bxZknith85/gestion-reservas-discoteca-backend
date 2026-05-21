from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, username, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("usuario", max_length=255)
    email = models.EmailField("correo", max_length=255, unique=True)
    phone_number = models.CharField("teléfono", max_length=50, unique=True)
    type_user = models.ForeignKey(
        "catalog.TypeUser",
        on_delete=models.PROTECT,
        db_column="type_user_id",
        verbose_name="tipo de usuario",
    )
    fcm_token = models.TextField("token FCM", null=True, blank=True)
    is_active = models.BooleanField("activo", default=True)
    is_staff = models.BooleanField("staff", default=False)
    created_at = models.DateTimeField("creado en", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado en", auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]

    class Meta:
        db_table = '"core"."users"'
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        indexes = [
            models.Index(fields=["type_user"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return f"{self.username} ({self.email})"


class Event(models.Model):
    name = models.CharField("nombre", max_length=300)
    description = models.TextField("descripción", null=True, blank=True)
    flyer_url = models.TextField("URL del flyer", null=True, blank=True)
    start_time = models.DateTimeField("inicio")
    end_time = models.DateTimeField("fin")
    event_state = models.ForeignKey(
        "catalog.EventState",
        on_delete=models.SET_NULL,
        db_column="event_state_id",
        null=True,
        blank=True,
        verbose_name="estado",
    )
    created_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        db_column="created_by",
        null=True,
        blank=True,
        verbose_name="creado por",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"core"."events"'
        verbose_name = "evento"
        verbose_name_plural = "eventos"
        indexes = [
            models.Index(fields=["event_state"]),
            models.Index(fields=["start_time"]),
        ]

    def __str__(self):
        return self.name


class DicoTable(models.Model):
    number = models.IntegerField("número", unique=True)
    table_type = models.ForeignKey(
        "catalog.TableType",
        on_delete=models.PROTECT,
        db_column="table_type_id",
        verbose_name="tipo",
    )
    capacity = models.IntegerField("capacidad")
    table_state = models.ForeignKey(
        "catalog.TableState",
        on_delete=models.PROTECT,
        db_column="table_state_id",
        verbose_name="estado",
    )

    class Meta:
        db_table = '"core"."dico_tables"'
        verbose_name = "mesa"
        verbose_name_plural = "mesas"

    def __str__(self):
        return f"Mesa {self.number} ({self.capacity} pers.)"


class TypeTicket(models.Model):
    name = models.CharField("nombre", max_length=200)
    event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        db_column="event_id",
        related_name="type_tickets",
        verbose_name="evento",
    )
    available_quantity = models.IntegerField("cantidad disponible")
    max_override = models.IntegerField("máx. por persona", null=True, blank=True)
    price = models.DecimalField("precio", max_digits=10, decimal_places=2)

    class Meta:
        db_table = '"core"."type_tickets"'
        verbose_name = "tipo de ticket"
        verbose_name_plural = "tipos de ticket"
        indexes = [
            models.Index(fields=["event"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.event.name}"


class TablePrice(models.Model):
    table = models.ForeignKey(
        "core.DicoTable",
        on_delete=models.CASCADE,
        db_column="table_id",
        related_name="table_prices",
        verbose_name="mesa",
    )
    event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        db_column="event_id",
        related_name="table_prices",
        verbose_name="evento",
    )
    price = models.DecimalField("precio", max_digits=10, decimal_places=2)

    class Meta:
        db_table = '"core"."table_prices"'
        verbose_name = "precio de mesa"
        verbose_name_plural = "precios de mesa"
        constraints = [
            models.UniqueConstraint(fields=["table", "event"], name="uq_table_event_price")
        ]
        indexes = [
            models.Index(fields=["table"]),
            models.Index(fields=["event"]),
        ]

    def __str__(self):
        return f"Mesa {self.table.number} - {self.event.name}: ${self.price}"
