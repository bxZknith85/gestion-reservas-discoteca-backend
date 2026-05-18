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
    def test_crear(self, client):
        response = client.post(BASE + "/", json=ORDER_DETAIL_DATA)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["order_id"] == ORDER_DETAIL_DATA["order_id"]
        assert data["quantity"] == ORDER_DETAIL_DATA["quantity"]
        assert "id" in data

    def test_crear_datos_invalidos(self, client):
        response = client.post(BASE + "/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetOrderDetail:
    def test_obtener(self, client):
        response = client.get(f"{BASE}/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1

    def test_obtener_no_existente(self, client):
        response = client.get(f"{BASE}/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Detalle de orden no encontrado" in response.json()["detail"]


class TestListOrderDetails:
    def test_listar(self, client):
        response = client.get(BASE + "/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_listar_por_orden(self, client):
        response = client.get(f"{BASE}/order/2")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestUpdateOrderDetail:
    def test_actualizar(self, client):
        response = client.put(f"{BASE}/1", json=ORDER_DETAIL_UPDATE)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["quantity"] == ORDER_DETAIL_UPDATE["quantity"]

    def test_actualizar_no_existente(self, client):
        response = client.put(f"{BASE}/999", json=ORDER_DETAIL_UPDATE)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Detalle de orden no encontrado" in response.json()["detail"]


class TestDeleteOrderDetail:
    def test_eliminar(self, client):
        response = client.delete(f"{BASE}/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_eliminar_no_existente(self, client):
        response = client.delete(f"{BASE}/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Detalle de orden no encontrado" in response.json()["detail"]
