from django.db.models import Count, Q, Sum
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.core.models import DicoTable, Event, TablePrice, TypeTicket, User
from apps.core.serializers import (
    DicoTableSerializer,
    EventSerializer,
    TablePriceSerializer,
    TypeTicketSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from apps.transactions.models import Order, Payment, Reservation, Ticket


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "partial_update" or self.action == "update":
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if self.action == "list" and user.type_user_id != 2:
            return User.objects.filter(id=user.id)
        return super().get_queryset()

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        search = params.get("search")
        if search:
            qs = qs.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        state = params.get("state")
        if state:
            qs = qs.filter(event_state_id=state)

        date_from = params.get("date_from")
        if date_from:
            qs = qs.filter(start_time__gte=date_from)

        date_to = params.get("date_to")
        if date_to:
            qs = qs.filter(end_time__lte=date_to)

        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DicoTableViewSet(viewsets.ModelViewSet):
    queryset = DicoTable.objects.all()
    serializer_class = DicoTableSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        table_type = params.get("table_type")
        if table_type:
            qs = qs.filter(table_type_id=table_type)

        table_state = params.get("table_state")
        if table_state:
            qs = qs.filter(table_state_id=table_state)

        capacity_min = params.get("capacity_min")
        if capacity_min:
            qs = qs.filter(capacity__gte=capacity_min)

        return qs


class TypeTicketViewSet(viewsets.ModelViewSet):
    queryset = TypeTicket.objects.all()
    serializer_class = TypeTicketSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        event_id = self.request.query_params.get("event")
        if event_id:
            qs = qs.filter(event_id=event_id)
        return qs


class TablePriceViewSet(viewsets.ModelViewSet):
    queryset = TablePrice.objects.all()
    serializer_class = TablePriceSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        event_id = self.request.query_params.get("event")
        table_id = self.request.query_params.get("table")
        if event_id:
            qs = qs.filter(event_id=event_id)
        if table_id:
            qs = qs.filter(table_id=table_id)
        return qs


@api_view(["GET"])
@permission_classes([AllowAny])
def reservation_availability_view(request):
    table_id = request.query_params.get("table")
    event_id = request.query_params.get("event")

    if not table_id or not event_id:
        return Response(
            {"detail": "Se requieren los parámetros 'table' y 'event'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        table = DicoTable.objects.get(id=table_id)
    except DicoTable.DoesNotExist:
        return Response(
            {"detail": "La mesa no existe."},
            status=status.HTTP_404_NOT_FOUND,
        )

    reserved = Reservation.objects.filter(
        table_id=table_id, event_id=event_id,
        reservation_state_id__in=[1, 2],
    ).exists()

    return Response({
        "table_id": table.id,
        "table_number": table.number,
        "event_id": int(event_id),
        "available": not reserved,
        "capacity": table.capacity,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats_view(request):
    now = timezone.now()
    total_users = User.objects.count()
    total_events = Event.objects.count()
    active_events = Event.objects.filter(event_state_id=1).count()
    total_reservations = Reservation.objects.count()
    pending_reservations = Reservation.objects.filter(reservation_state_id=1).count()
    total_tickets = Ticket.objects.count()
    total_orders = Order.objects.count()
    paid_orders = Order.objects.filter(status="paid").count()
    total_revenue = Payment.objects.filter(
        status="confirmed",
    ).aggregate(total=Sum("amount"))["total"] or 0

    return Response({
        "total_users": total_users,
        "total_events": total_events,
        "active_events": active_events,
        "total_reservations": total_reservations,
        "pending_reservations": pending_reservations,
        "total_tickets": total_tickets,
        "total_orders": total_orders,
        "paid_orders": paid_orders,
        "total_revenue": total_revenue,
    })
