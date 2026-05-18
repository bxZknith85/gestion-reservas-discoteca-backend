from fastapi import status

BASE = "/api/v1/order-details"

ORDER_DETAIL_DATA = {
    "order_id": 2,
    "type_ticket_id": 2,
    "quantity": 2,
    "unit_price": "50.00",
}

ORDER_DETAIL_UPDATE = {
    "quantity": 3,
    "unit_price": "45.00",
}


class TestCreateOrderDetail:
    def test_crear(self, client, auth_headers):
        response = client.post(BASE + "/", json=ORDER_DETAIL_DATA, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["order_id"] == ORDER_DETAIL_DATA["order_id"]
        assert data["quantity"] == ORDER_DETAIL_DATA["quantity"]
        assert "id" in data

    def test_crear_datos_invalidos(self, client, auth_headers):
        response = client.post(BASE + "/", json={}, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetOrderDetail:
    def test_obtener(self, client, auth_headers):
        response = client.get(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1

    def test_obtener_no_existente(self, client, auth_headers):
        response = client.get(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Detalle de orden no encontrado" in response.json()["detail"]


class TestListOrderDetails:
    def test_listar(self, client, auth_headers):
        response = client.get(BASE + "/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_listar_por_orden(self, client, auth_headers):
        response = client.get(f"{BASE}/order/2", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestUpdateOrderDetail:
    def test_actualizar(self, client, auth_headers):
        response = client.put(f"{BASE}/1", json=ORDER_DETAIL_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity"] == ORDER_DETAIL_UPDATE["quantity"]

    def test_actualizar_no_existente(self, client, auth_headers):
        response = client.put(f"{BASE}/999", json=ORDER_DETAIL_UPDATE, headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Detalle de orden no encontrado" in response.json()["detail"]


class TestDeleteOrderDetail:
    def test_eliminar(self, client, auth_headers):
        response = client.delete(f"{BASE}/1", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_eliminar_no_existente(self, client, auth_headers):
        response = client.delete(f"{BASE}/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Detalle de orden no encontrado" in response.json()["detail"]
