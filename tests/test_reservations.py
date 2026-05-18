from fastapi import status

BASE = "/api/v1/reservations"

RESERVATION_DATA = {
    "reservation_state_id": 1,
    "user_id": 2,
    "table_id": 2,
    "event_id": 2,
}

RESERVATION_UPDATE = {
    "reservation_state_id": 2,
}


class TestCreateReservation:
    def test_crear_reserva(self, client):
        response = client.post(BASE + "/", json=RESERVATION_DATA)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user_id"] == RESERVATION_DATA["user_id"]
        assert data["table_id"] == RESERVATION_DATA["table_id"]
        assert "id" in data

    def test_crear_reserva_datos_invalidos(self, client):
        response = client.post(BASE + "/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetReservation:
    def test_obtener_reserva(self, client):
        response = client.get(f"{BASE}/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1

    def test_obtener_reserva_no_existente(self, client):
        response = client.get(f"{BASE}/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Reserva no encontrada" in response.json()["detail"]


class TestListReservations:
    def test_listar_reservas(self, client):
        response = client.get(BASE + "/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_listar_reservas_por_usuario(self, client):
        response = client.get(f"{BASE}/user/2")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestUpdateReservation:
    def test_actualizar_reserva(self, client):
        response = client.put(f"{BASE}/1", json=RESERVATION_UPDATE)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["reservation_state_id"] == RESERVATION_UPDATE["reservation_state_id"]

    def test_actualizar_reserva_no_existente(self, client):
        response = client.put(f"{BASE}/999", json=RESERVATION_UPDATE)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Reserva no encontrada" in response.json()["detail"]


class TestDeleteReservation:
    def test_eliminar_reserva(self, client):
        response = client.delete(f"{BASE}/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_eliminar_reserva_no_existente(self, client):
        response = client.delete(f"{BASE}/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Reserva no encontrada" in response.json()["detail"]
