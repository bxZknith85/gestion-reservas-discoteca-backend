from fastapi import status

BASE = "/api/v1/type-tickets"

TYPE_TICKET_DATA = {
    "name": "General",
    "event_id": 3,
    "available_quantity": 100,
    "price": "50.00",
}

TYPE_TICKET_UPDATE = {
    "price": "60.00",
    "available_quantity": 80,
}


class TestCreateTypeTicket:
    def test_crear(self, client, auth_headers):
        response = client.post(BASE + "/", json=TYPE_TICKET_DATA, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == TYPE_TICKET_DATA["name"]
        assert data["event_id"] == TYPE_TICKET_DATA["event_id"]
        assert "id" in data

    def test_crear_datos_invalidos(self, client, auth_headers):
        response = client.post(BASE + "/", json={"name": ""}, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetTypeTicket:
    def test_obtener(self, client, auth_headers):
        response = client.get(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1

    def test_obtener_no_existente(self, client, auth_headers):
        response = client.get(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Tipo de ticket no encontrado" in response.json()["detail"]


class TestListTypeTickets:
    def test_listar(self, client, auth_headers):
        response = client.get(BASE + "/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_listar_por_evento(self, client, auth_headers):
        response = client.get(f"{BASE}/event/3", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestUpdateTypeTicket:
    def test_actualizar(self, client, auth_headers):
        response = client.put(f"{BASE}/1", json=TYPE_TICKET_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["price"] == TYPE_TICKET_UPDATE["price"]

    def test_actualizar_no_existente(self, client, auth_headers):
        response = client.put(f"{BASE}/999", json=TYPE_TICKET_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Tipo de ticket no encontrado" in response.json()["detail"]


class TestDeleteTypeTicket:
    def test_eliminar(self, client, auth_headers):
        response = client.delete(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_eliminar_no_existente(self, client, auth_headers):
        response = client.delete(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Tipo de ticket no encontrado" in response.json()["detail"]
