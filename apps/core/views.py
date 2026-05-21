from rest_framework import viewsets
from rest_framework.decorators import action
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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DicoTableViewSet(viewsets.ModelViewSet):
    queryset = DicoTable.objects.all()
    serializer_class = DicoTableSerializer


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
