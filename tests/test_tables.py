from fastapi import status

BASE = "/api/v1/tables"

TABLE_DATA = {
    "number": 1,
    "table_type_id": 1,
    "capacity": 4,
    "table_state_id": 1,
}

TABLE_UPDATE = {
    "capacity": 6,
    "table_state_id": 2,
}


class TestCreateTable:
    def test_crear_mesa(self, client, auth_headers):
        response = client.post(BASE + "/", json=TABLE_DATA, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["number"] == TABLE_DATA["number"]
        assert data["capacity"] == TABLE_DATA["capacity"]
        assert "id" in data

    def test_crear_mesa_numero_duplicado(self, client, auth_headers):
        response = client.post(BASE + "/", json=TABLE_DATA, headers=auth_headers)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "Ya existe una mesa con el número" in response.json()["detail"]

    def test_crear_mesa_datos_invalidos(self, client, auth_headers):
        response = client.post(BASE + "/", json={"number": -1}, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetTable:
    def test_obtener_mesa(self, client, auth_headers):
        response = client.get(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["number"] == TABLE_DATA["number"]

    def test_obtener_mesa_no_existente(self, client, auth_headers):
        response = client.get(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Mesa no encontrada" in response.json()["detail"]


class TestListTables:
    def test_listar_mesas(self, client, auth_headers):
        response = client.get(BASE + "/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1


class TestUpdateTable:
    def test_actualizar_mesa(self, client, auth_headers):
        response = client.put(f"{BASE}/1", json=TABLE_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["capacity"] == TABLE_UPDATE["capacity"]

    def test_actualizar_mesa_no_existente(self, client, auth_headers):
        response = client.put(f"{BASE}/999", json=TABLE_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Mesa no encontrada" in response.json()["detail"]


class TestDeleteTable:
    def test_eliminar_mesa(self, client, auth_headers):
        response = client.delete(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_eliminar_mesa_no_existente(self, client, auth_headers):
        response = client.delete(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Mesa no encontrada" in response.json()["detail"]
