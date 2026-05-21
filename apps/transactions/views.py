from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.transactions.models import (
    Order,
    OrderDetail,
    Payment,
    Reservation,
    Ticket,
)
from apps.transactions.serializers import (
    OrderDetailSerializer,
    OrderSerializer,
    PaymentSerializer,
    ReservationSerializer,
    TicketSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.query_params.get("user")
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs

    @action(detail=True, methods=["get", "post"])
    def payments(self, request, pk=None):  # noqa: ARG002
        order = self.get_object()
        if request.method == "GET":
            payments = order.payments.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            if order.user_id != request.user.id:
                return Response(
                    {"detail": "No tienes permiso para agregar pagos a esta orden."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(order=order)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ["put", "patch", "get"]

    def get_queryset(self):
        qs = super().get_queryset()
        order_id = self.request.query_params.get("order")
        if order_id:
            qs = qs.filter(order_id=order_id)
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        return qs


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.query_params.get("user")
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.query_params.get("user")
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        order_id = self.request.query_params.get("order")
        if order_id:
            qs = qs.filter(order_id=order_id)
        return qs
