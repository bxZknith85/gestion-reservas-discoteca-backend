import pytest


@pytest.mark.django_db
class TestCreateEvent:
    def test_create_event_success(self, auth_client, event_data):
        response = auth_client.post("/api/v1/events/", event_data, format="json")
        assert response.status_code == 201
        assert response.data["name"] == event_data["name"]

    def test_create_event_unauthenticated(self, api_client, event_data):
        response = api_client.post("/api/v1/events/", event_data, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestGetEvent:
    def test_get_event_public(self, api_client, test_event):
        response = api_client.get(f"/api/v1/events/{test_event.id}/")
        assert response.status_code == 200
        assert response.data["name"] == test_event.name

    def test_get_nonexistent_event(self, api_client):
        response = api_client.get("/api/v1/events/99999/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestListEvents:
    def test_list_events_public(self, api_client, test_event):
        response = api_client.get("/api/v1/events/")
        assert response.status_code == 200

    def test_list_events_empty(self, api_client):
        response = api_client.get("/api/v1/events/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestUpdateEvent:
    def test_update_event(self, auth_client, test_event):
        response = auth_client.put(
            f"/api/v1/events/{test_event.id}/",
            {"name": "Evento Actualizado", "start_time": "2026-06-15T22:00:00-05:00",
             "end_time": "2026-06-16T04:00:00-05:00"},
            format="json",
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestDeleteEvent:
    def test_delete_event(self, auth_client, test_event):
        response = auth_client.delete(f"/api/v1/events/{test_event.id}/")
        assert response.status_code == 204
