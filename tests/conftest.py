import pytest
from rest_framework.test import APIClient

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
from apps.core.models import User


@pytest.fixture(autouse=True)
def seed_catalog_data():
    TypeUser.objects.get_or_create(id=1, name="cliente")
    TypeUser.objects.get_or_create(id=2, name="admin")
    TypeUser.objects.get_or_create(id=3, name="staff")
    EventState.objects.get_or_create(id=1, name="activo")
    EventState.objects.get_or_create(id=2, name="cancelado")
    EventState.objects.get_or_create(id=3, name="finalizado")
    EventState.objects.get_or_create(id=4, name="borrador")
    ReservationState.objects.get_or_create(id=1, name="pendiente")
    ReservationState.objects.get_or_create(id=2, name="confirmada")
    ReservationState.objects.get_or_create(id=3, name="expirada")
    ReservationState.objects.get_or_create(id=4, name="cancelada")
    TableState.objects.get_or_create(id=1, name="disponible")
    TableState.objects.get_or_create(id=2, name="reservada")
    TableState.objects.get_or_create(id=3, name="fuera_de_servicio")
    TableType.objects.get_or_create(id=1, name="regular")
    TableType.objects.get_or_create(id=2, name="vip")
    TableType.objects.get_or_create(id=3, name="terraza")
    TableType.objects.get_or_create(id=4, name="privada")
    TicketState.objects.get_or_create(id=1, name="activo")
    TicketState.objects.get_or_create(id=2, name="usado")
    TicketState.objects.get_or_create(id=3, name="cancelado")
    PaymentMethod.objects.get_or_create(id=1, name="efectivo")
    PaymentMethod.objects.get_or_create(id=2, name="transferencia_bancaria")
    PaymentMethod.objects.get_or_create(id=3, name="nequi")
    PaymentMethod.objects.get_or_create(id=4, name="daviplata")
    PaymentMethod.objects.get_or_create(id=5, name="tarjeta_credito")
    PaymentMethod.objects.get_or_create(id=6, name="tarjeta_debito")
    OrderStatus.objects.get_or_create(id=1, name="pending")
    OrderStatus.objects.get_or_create(id=2, name="paid")
    OrderStatus.objects.get_or_create(id=3, name="cancelled")
    OrderStatus.objects.get_or_create(id=4, name="refunded")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "phone_number": "3001234567",
        "password": "testpass123",
        "type_user": 1,
    }


@pytest.fixture
def test_user(db, user_data):
    return User.objects.create_user(
        email=user_data["email"],
        username=user_data["username"],
        phone_number=user_data["phone_number"],
        password=user_data["password"],
        type_user_id=user_data["type_user"],
    )


@pytest.fixture
def auth_client(api_client, test_user, user_data):
    response = api_client.post("/api/v1/auth/login/", {
        "email": user_data["email"],
        "password": user_data["password"],
    })
    token = response.data["access_token"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture
def event_data():
    return {
        "name": "Fiesta de prueba",
        "description": "Descripción",
        "start_time": "2026-06-15T22:00:00-05:00",
        "end_time": "2026-06-16T04:00:00-05:00",
        "event_state": 1,
    }


@pytest.fixture
def test_event(db, event_data):
    from apps.core.models import Event
    return Event.objects.create(
        name=event_data["name"],
        description=event_data["description"],
        start_time=event_data["start_time"],
        end_time=event_data["end_time"],
        event_state_id=event_data["event_state"],
    )


@pytest.fixture
def table_data():
    return {
        "number": 1,
        "table_type": 1,
        "capacity": 4,
        "table_state": 1,
    }


@pytest.fixture
def test_table(db, table_data):
    from apps.core.models import DicoTable
    return DicoTable.objects.create(
        number=table_data["number"],
        capacity=table_data["capacity"],
        table_type_id=table_data["table_type"],
        table_state_id=table_data["table_state"],
    )
