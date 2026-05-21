from rest_framework import viewsets
from rest_framework.permissions import AllowAny

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
from apps.catalog.serializers import (
    EventStateSerializer,
    OrderStatusSerializer,
    PaymentMethodSerializer,
    ReservationStateSerializer,
    TableStateSerializer,
    TableTypeSerializer,
    TicketStateSerializer,
    TypeUserSerializer,
)


class TypeUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TypeUser.objects.all()
    serializer_class = TypeUserSerializer
    permission_classes = [AllowAny]


class EventStateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EventState.objects.all()
    serializer_class = EventStateSerializer
    permission_classes = [AllowAny]


class ReservationStateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReservationState.objects.all()
    serializer_class = ReservationStateSerializer
    permission_classes = [AllowAny]


class TableStateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TableState.objects.all()
    serializer_class = TableStateSerializer
    permission_classes = [AllowAny]


class TableTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer
    permission_classes = [AllowAny]


class TicketStateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TicketState.objects.all()
    serializer_class = TicketStateSerializer
    permission_classes = [AllowAny]


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [AllowAny]


class OrderStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [AllowAny]
