from django.db import models


class Order(models.Model):
    user = models.ForeignKey(
        "core.User",
        on_delete=models.PROTECT,
        db_column="user_id",
        related_name="orders",
        verbose_name="usuario",
    )
    ordered_at = models.DateTimeField("fecha de orden", auto_now_add=True)
    total = models.DecimalField("total", max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        "estado",
        max_length=20,
        default="pending",
        choices=[
            ("pending", "Pendiente"),
            ("paid", "Pagado"),
            ("cancelled", "Cancelado"),
            ("refunded", "Reembolsado"),
        ],
    )
    notes = models.TextField("notas", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"transactions"."orders"'
        verbose_name = "orden"
        verbose_name_plural = "órdenes"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Orden #{self.id} - {self.user.username} - {self.status}"


class Reservation(models.Model):
    reservation_state = models.ForeignKey(
        "catalog.ReservationState",
        on_delete=models.PROTECT,
        db_column="reservation_state_id",
        verbose_name="estado",
    )
    user = models.ForeignKey(
        "core.User",
        on_delete=models.PROTECT,
        db_column="user_id",
        related_name="reservations",
        verbose_name="usuario",
    )
    table = models.ForeignKey(
        "core.DicoTable",
        on_delete=models.PROTECT,
        db_column="table_id",
        related_name="reservations",
        verbose_name="mesa",
    )
    event = models.ForeignKey(
        "core.Event",
        on_delete=models.SET_NULL,
        db_column="event_id",
        null=True,
        blank=True,
        related_name="reservations",
        verbose_name="evento",
    )
    reserved_at = models.DateTimeField("reservado en", auto_now_add=True)
    expires_at = models.DateTimeField("expira en", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"transactions"."reservations"'
        verbose_name = "reserva"
        verbose_name_plural = "reservas"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["table"]),
            models.Index(fields=["event"]),
            models.Index(fields=["reservation_state"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self):
        return f"Reserva #{self.id} - Mesa {self.table.number} - {self.user.username}"


class Ticket(models.Model):
    user = models.ForeignKey(
        "core.User",
        on_delete=models.PROTECT,
        db_column="user_id",
        related_name="tickets",
        verbose_name="usuario",
    )
    type_ticket = models.ForeignKey(
        "core.TypeTicket",
        on_delete=models.PROTECT,
        db_column="type_ticket_id",
        verbose_name="tipo de ticket",
    )
    ticket_state = models.ForeignKey(
        "catalog.TicketState",
        on_delete=models.PROTECT,
        db_column="ticket_state_id",
        verbose_name="estado",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"transactions"."tickets"'
        verbose_name = "ticket"
        verbose_name_plural = "tickets"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["type_ticket"]),
            models.Index(fields=["ticket_state"]),
        ]

    def __str__(self):
        return f"Ticket #{self.id} - {self.type_ticket.name} - {self.user.username}"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        "transactions.Order",
        on_delete=models.CASCADE,
        db_column="order_id",
        related_name="order_details",
        verbose_name="orden",
    )
    ticket = models.ForeignKey(
        "transactions.Ticket",
        on_delete=models.SET_NULL,
        db_column="ticket_id",
        null=True,
        blank=True,
        related_name="order_details",
        verbose_name="ticket",
    )
    reservation = models.ForeignKey(
        "transactions.Reservation",
        on_delete=models.SET_NULL,
        db_column="reservation_id",
        null=True,
        blank=True,
        related_name="order_details",
        verbose_name="reserva",
    )
    type_ticket = models.ForeignKey(
        "core.TypeTicket",
        on_delete=models.SET_NULL,
        db_column="type_ticket_id",
        null=True,
        blank=True,
        verbose_name="tipo de ticket",
    )
    table = models.ForeignKey(
        "core.DicoTable",
        on_delete=models.SET_NULL,
        db_column="table_id",
        null=True,
        blank=True,
        verbose_name="mesa",
    )
    quantity = models.IntegerField("cantidad", default=1)
    unit_price = models.DecimalField("precio unitario", max_digits=10, decimal_places=2)
    discount = models.DecimalField("descuento", max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = '"transactions"."order_details"'
        verbose_name = "detalle de orden"
        verbose_name_plural = "detalles de orden"
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["ticket"]),
            models.Index(fields=["reservation"]),
        ]

    def __str__(self):
        return f"Detalle #{self.id} - Orden #{self.order_id}"


class Payment(models.Model):
    order = models.ForeignKey(
        "transactions.Order",
        on_delete=models.PROTECT,
        db_column="order_id",
        related_name="payments",
        verbose_name="orden",
    )
    payment_method = models.ForeignKey(
        "catalog.PaymentMethod",
        on_delete=models.PROTECT,
        db_column="payment_method_id",
        verbose_name="método de pago",
    )
    amount = models.DecimalField("monto", max_digits=10, decimal_places=2)
    status = models.CharField(
        "estado",
        max_length=20,
        default="pending",
        choices=[
            ("pending", "Pendiente"),
            ("confirmed", "Confirmado"),
            ("rejected", "Rechazado"),
            ("refunded", "Reembolsado"),
        ],
    )
    voucher_url = models.TextField("URL del comprobante", null=True, blank=True)
    reference_number = models.TextField("número de referencia", null=True, blank=True)
    confirmed_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        db_column="confirmed_by",
        null=True,
        blank=True,
        related_name="payments_confirmed",
        verbose_name="confirmado por",
    )
    confirmed_at = models.DateTimeField("confirmado en", null=True, blank=True)
    notes = models.TextField("notas", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"transactions"."payments"'
        verbose_name = "pago"
        verbose_name_plural = "pagos"
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Pago #{self.id} - Orden #{self.order_id} - ${self.amount}"
