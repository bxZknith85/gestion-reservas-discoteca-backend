from fastapi import status

BASE = "/api/v1/tickets"

TICKET_DATA = {
    "user_id": 4,
    "type_ticket_id": 2,
    "ticket_state_id": 1,
}

TICKET_UPDATE = {
    "ticket_state_id": 2,
}


class TestCreateTicket:
    def test_crear(self, client, auth_headers):
        response = client.post(BASE + "/", json=TICKET_DATA, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user_id"] == TICKET_DATA["user_id"]
        assert data["type_ticket_id"] == TICKET_DATA["type_ticket_id"]
        assert "id" in data

    def test_crear_datos_invalidos(self, client, auth_headers):
        response = client.post(BASE + "/", json={}, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetTicket:
    def test_obtener(self, client, auth_headers):
        response = client.get(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1

    def test_obtener_no_existente(self, client, auth_headers):
        response = client.get(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Ticket no encontrado" in response.json()["detail"]


class TestListTickets:
    def test_listar(self, client, auth_headers):
        response = client.get(BASE + "/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_listar_por_usuario(self, client, auth_headers):
        response = client.get(f"{BASE}/user/4", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestUpdateTicket:
    def test_actualizar(self, client, auth_headers):
        response = client.put(f"{BASE}/1", json=TICKET_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["ticket_state_id"] == TICKET_UPDATE["ticket_state_id"]

    def test_actualizar_no_existente(self, client, auth_headers):
        response = client.put(f"{BASE}/999", json=TICKET_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Ticket no encontrado" in response.json()["detail"]


class TestDeleteTicket:
    def test_eliminar(self, client, auth_headers):
        response = client.delete(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_eliminar_no_existente(self, client, auth_headers):
        response = client.delete(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Ticket no encontrado" in response.json()["detail"]
