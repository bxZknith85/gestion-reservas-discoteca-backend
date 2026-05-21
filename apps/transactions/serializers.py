from rest_framework import serializers

from apps.transactions.models import (
    Order,
    OrderDetail,
    Payment,
    Reservation,
    Ticket,
)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id", "user", "ordered_at", "total",
            "status", "notes", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "ordered_at", "created_at", "updated_at"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id", "reservation_state", "user", "table", "event",
            "reserved_at", "expires_at", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "reserved_at", "created_at", "updated_at"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id", "user", "type_ticket", "ticket_state",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = [
            "id", "order", "ticket", "reservation",
            "type_ticket", "table", "quantity",
            "unit_price", "discount",
        ]
        read_only_fields = ["id"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id", "order", "payment_method", "amount", "status",
            "voucher_url", "reference_number", "confirmed_by",
            "confirmed_at", "notes", "created_at",
        ]
        read_only_fields = ["id", "confirmed_at", "created_at"]
