import pytest


@pytest.mark.django_db
class TestCreateTicket:
    def test_create_success(self, auth_client, test_user, test_event):
        from apps.core.models import TypeTicket
        tt = TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        data = {"user": test_user.id, "type_ticket": tt.id, "ticket_state": 1}
        response = auth_client.post("/api/v1/tickets/", data, format="json")
        assert response.status_code == 201

    def test_create_unauthenticated(self, api_client, test_user, test_event):
        from apps.core.models import TypeTicket
        tt = TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        data = {"user": test_user.id, "type_ticket": tt.id, "ticket_state": 1}
        response = api_client.post("/api/v1/tickets/", data, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestGetTicket:
    def test_get(self, auth_client, test_user, test_event):
        from apps.core.models import TypeTicket
        from apps.transactions.models import Ticket
        tt = TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        ticket = Ticket.objects.create(user=test_user, type_ticket=tt, ticket_state_id=1)
        response = auth_client.get(f"/api/v1/tickets/{ticket.id}/")
        assert response.status_code == 200

    def test_get_nonexistent(self, auth_client):
        response = auth_client.get("/api/v1/tickets/99999/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestListTickets:
    def test_list(self, auth_client, test_user, test_event):
        from apps.core.models import TypeTicket
        from apps.transactions.models import Ticket
        tt = TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        Ticket.objects.create(user=test_user, type_ticket=tt, ticket_state_id=1)
        response = auth_client.get("/api/v1/tickets/")
        assert response.status_code == 200

    def test_list_by_user(self, auth_client, test_user, test_event):
        from apps.core.models import TypeTicket
        from apps.transactions.models import Ticket
        tt = TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        Ticket.objects.create(user=test_user, type_ticket=tt, ticket_state_id=1)
        response = auth_client.get(f"/api/v1/tickets/?user={test_user.id}")
        assert response.status_code == 200


@pytest.mark.django_db
class TestUpdateTicket:
    def test_update(self, auth_client, test_user, test_event):
        from apps.core.models import TypeTicket
        from apps.transactions.models import Ticket
        tt = TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        ticket = Ticket.objects.create(user=test_user, type_ticket=tt, ticket_state_id=1)
        response = auth_client.put(
            f"/api/v1/tickets/{ticket.id}/",
            {"user": test_user.id, "type_ticket": tt.id, "ticket_state": 3},
            format="json",
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestDeleteTicket:
    def test_delete(self, auth_client, test_user, test_event):
        from apps.core.models import TypeTicket
        from apps.transactions.models import Ticket
        tt = TypeTicket.objects.create(name="General", event=test_event, available_quantity=100, price="50000")
        ticket = Ticket.objects.create(user=test_user, type_ticket=tt, ticket_state_id=1)
        response = auth_client.delete(f"/api/v1/tickets/{ticket.id}/")
        assert response.status_code == 204
