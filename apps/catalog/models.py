from django.db import models


class TypeUser(models.Model):
    name = models.CharField("nombre", max_length=100)

    class Meta:
        db_table = '"catalog"."type_users"'
        verbose_name = "tipo de usuario"
        verbose_name_plural = "tipos de usuario"

    def __str__(self):
        return self.name


class EventState(models.Model):
    name = models.CharField("nombre", max_length=100)

    class Meta:
        db_table = '"catalog"."event_states"'
        verbose_name = "estado de evento"
        verbose_name_plural = "estados de evento"

    def __str__(self):
        return self.name


class ReservationState(models.Model):
    name = models.CharField("nombre", max_length=100)

    class Meta:
        db_table = '"catalog"."reservation_states"'
        verbose_name = "estado de reserva"
        verbose_name_plural = "estados de reserva"

    def __str__(self):
        return self.name


class TableState(models.Model):
    name = models.CharField("nombre", max_length=100)

    class Meta:
        db_table = '"catalog"."table_states"'
        verbose_name = "estado de mesa"
        verbose_name_plural = "estados de mesa"

    def __str__(self):
        return self.name


class TableType(models.Model):
    name = models.CharField("nombre", max_length=100)

    class Meta:
        db_table = '"catalog"."table_types"'
        verbose_name = "tipo de mesa"
        verbose_name_plural = "tipos de mesa"

    def __str__(self):
        return self.name


class TicketState(models.Model):
    name = models.CharField("nombre", max_length=100)

    class Meta:
        db_table = '"catalog"."ticket_states"'
        verbose_name = "estado de ticket"
        verbose_name_plural = "estados de ticket"

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField("nombre", max_length=100)

    class Meta:
        db_table = '"catalog"."payment_methods"'
        verbose_name = "método de pago"
        verbose_name_plural = "métodos de pago"

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    name = models.CharField("nombre", max_length=100)

    class Meta:
        db_table = '"catalog"."order_statuses"'
        verbose_name = "estado de orden"
        verbose_name_plural = "estados de orden"

    def __str__(self):
        return self.name
