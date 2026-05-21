import pytest


@pytest.mark.django_db
class TestCreateReservation:
    def test_create_success(self, auth_client, test_user, test_table, test_event):
        data = {
            "reservation_state": 1,
            "user": test_user.id,
            "table": test_table.id,
            "event": test_event.id,
        }
        response = auth_client.post("/api/v1/reservations/", data, format="json")
        assert response.status_code == 201

    def test_create_unauthenticated(self, api_client, test_user, test_table, test_event):
        data = {
            "reservation_state": 1,
            "user": test_user.id,
            "table": test_table.id,
            "event": test_event.id,
        }
        response = api_client.post("/api/v1/reservations/", data, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestGetReservation:
    def test_get(self, auth_client, test_user, test_table):
        from apps.transactions.models import Reservation
        res = Reservation.objects.create(
            reservation_state_id=1, user=test_user, table=test_table
        )
        response = auth_client.get(f"/api/v1/reservations/{res.id}/")
        assert response.status_code == 200

    def test_get_nonexistent(self, auth_client):
        response = auth_client.get("/api/v1/reservations/99999/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestListReservations:
    def test_list(self, auth_client, test_user, test_table):
        from apps.transactions.models import Reservation
        Reservation.objects.create(reservation_state_id=1, user=test_user, table=test_table)
        response = auth_client.get("/api/v1/reservations/")
        assert response.status_code == 200

    def test_list_by_user(self, auth_client, test_user, test_table):
        from apps.transactions.models import Reservation
        Reservation.objects.create(reservation_state_id=1, user=test_user, table=test_table)
        response = auth_client.get(f"/api/v1/reservations/?user={test_user.id}")
        assert response.status_code == 200


@pytest.mark.django_db
class TestUpdateReservation:
    def test_update(self, auth_client, test_user, test_table):
        from apps.transactions.models import Reservation
        res = Reservation.objects.create(reservation_state_id=1, user=test_user, table=test_table)
        response = auth_client.put(
            f"/api/v1/reservations/{res.id}/",
            {"reservation_state": 4, "user": test_user.id, "table": test_table.id},
            format="json",
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestDeleteReservation:
    def test_delete(self, auth_client, test_user, test_table):
        from apps.transactions.models import Reservation
        res = Reservation.objects.create(reservation_state_id=1, user=test_user, table=test_table)
        response = auth_client.delete(f"/api/v1/reservations/{res.id}/")
        assert response.status_code == 204
