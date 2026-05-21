import pytest


@pytest.mark.django_db
class TestCreateTypeTicket:
    def test_create_type_ticket_success(self, auth_client, test_event):
        data = {"name": "General", "event": test_event.id, "available_quantity": 100, "price": "50000.00"}
        response = auth_client.post("/api/v1/type-tickets/", data, format="json")
        assert response.status_code == 201

    def test_create_type_ticket_unauthenticated(self, api_client, test_event):
        data = {"name": "VIP", "event": test_event.id, "available_quantity": 50, "price": "100000.00"}
        response = api_client.post("/api/v1/type-tickets/", data, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestGetTypeTicket:
    def test_get_type_ticket(self, auth_client, test_event):
        from apps.core.models import TypeTicket
        tt = TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        response = auth_client.get(f"/api/v1/type-tickets/{tt.id}/")
        assert response.status_code == 200

    def test_get_nonexistent(self, auth_client):
        response = auth_client.get("/api/v1/type-tickets/99999/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestListTypeTickets:
    def test_list(self, auth_client, test_event):
        from apps.core.models import TypeTicket
        TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        response = auth_client.get("/api/v1/type-tickets/")
        assert response.status_code == 200

    def test_list_by_event(self, auth_client, test_event):
        from apps.core.models import TypeTicket
        TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        response = auth_client.get(f"/api/v1/type-tickets/?event={test_event.id}")
        assert response.status_code == 200


@pytest.mark.django_db
class TestUpdateTypeTicket:
    def test_update(self, auth_client, test_event):
        from apps.core.models import TypeTicket
        tt = TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        response = auth_client.put(
            f"/api/v1/type-tickets/{tt.id}/",
            {"name": "VIP", "event": test_event.id, "available_quantity": 50, "price": "100000.00"},
            format="json",
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestDeleteTypeTicket:
    def test_delete(self, auth_client, test_event):
        from apps.core.models import TypeTicket
        tt = TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        response = auth_client.delete(f"/api/v1/type-tickets/{tt.id}/")
        assert response.status_code == 204
