from rest_framework import serializers

from apps.catalog.models import (
    EventState,
    OrderStatus,
    PaymentMethod,
    ReservationState,
    TableState,
    TableType,
    TicketState,
    TypeUser,
)


class TypeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeUser
        fields = ["id", "name"]


class EventStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventState
        fields = ["id", "name"]


class ReservationStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationState
        fields = ["id", "name"]


class TableStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableState
        fields = ["id", "name"]


class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = ["id", "name"]


class TicketStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketState
        fields = ["id", "name"]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "name"]


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ["id", "name"]
