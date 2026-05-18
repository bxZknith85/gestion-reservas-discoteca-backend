from fastapi import status

BASE = "/api/v1/table-prices"

TABLE_PRICE_DATA = {
    "table_id": 3,
    "event_id": 3,
    "price": "100.00",
}

TABLE_PRICE_UPDATE = {
    "price": "120.00",
}


class TestCreateTablePrice:
    def test_crear(self, client, auth_headers):
        response = client.post(BASE + "/", json=TABLE_PRICE_DATA, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["table_id"] == TABLE_PRICE_DATA["table_id"]
        assert data["event_id"] == TABLE_PRICE_DATA["event_id"]
        assert "id" in data

    def test_crear_duplicado(self, client, auth_headers):
        response = client.post(BASE + "/", json=TABLE_PRICE_DATA, headers=auth_headers)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "Ya existe un precio" in response.json()["detail"]

    def test_crear_datos_invalidos(self, client, auth_headers):
        response = client.post(BASE + "/", json={"table_id": -1}, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetTablePrice:
    def test_obtener(self, client, auth_headers):
        response = client.get(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1

    def test_obtener_no_existente(self, client, auth_headers):
        response = client.get(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Precio de mesa no encontrado" in response.json()["detail"]


class TestListTablePrices:
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

    def test_listar_por_mesa(self, client, auth_headers):
        response = client.get(f"{BASE}/table/3", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestUpdateTablePrice:
    def test_actualizar(self, client, auth_headers):
        response = client.put(f"{BASE}/1", json=TABLE_PRICE_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["price"] == TABLE_PRICE_UPDATE["price"]

    def test_actualizar_no_existente(self, client, auth_headers):
        response = client.put(f"{BASE}/999", json=TABLE_PRICE_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Precio de mesa no encontrado" in response.json()["detail"]


class TestDeleteTablePrice:
    def test_eliminar(self, client, auth_headers):
        response = client.delete(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_eliminar_no_existente(self, client, auth_headers):
        response = client.delete(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Precio de mesa no encontrado" in response.json()["detail"]
