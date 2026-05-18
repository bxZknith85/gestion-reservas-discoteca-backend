from fastapi import status

BASE = "/api/v1/events"

EVENT_DATA = {
    "name": "Fiesta de prueba",
    "description": "Descripción del evento",
    "start_time": "2026-06-15T22:00:00",
    "end_time": "2026-06-16T04:00:00",
    "event_state_id": 1,
}

EVENT_UPDATE = {
    "name": "Fiesta actualizada",
    "description": "Nueva descripción",
}


class TestCreateEvent:
    def test_crear_evento(self, client, auth_headers):
        response = client.post(BASE + "/", json=EVENT_DATA, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == EVENT_DATA["name"]
        assert "id" in data

    def test_crear_evento_datos_invalidos(self, client, auth_headers):
        response = client.post(BASE + "/", json={"name": ""}, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetEvent:
    def test_obtener_evento(self, client):
        response = client.get(f"{BASE}/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == EVENT_DATA["name"]

    def test_obtener_evento_no_existente(self, client):
        response = client.get(f"{BASE}/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Evento no encontrado" in response.json()["detail"]


class TestListEvents:
    def test_listar_eventos(self, client):
        response = client.get(BASE + "/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_listar_eventos_paginacion(self, client):
        response = client.get(BASE + "/?skip=0&limit=10")
        assert response.status_code == status.HTTP_200_OK


class TestUpdateEvent:
    def test_actualizar_evento(self, client, auth_headers):
        response = client.put(f"{BASE}/1", json=EVENT_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == EVENT_UPDATE["name"]

    def test_actualizar_evento_no_existente(self, client, auth_headers):
        response = client.put(f"{BASE}/999", json=EVENT_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Evento no encontrado" in response.json()["detail"]


class TestDeleteEvent:
    def test_eliminar_evento(self, client, auth_headers):
        response = client.delete(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_eliminar_evento_no_existente(self, client, auth_headers):
        response = client.delete(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Evento no encontrado" in response.json()["detail"]
