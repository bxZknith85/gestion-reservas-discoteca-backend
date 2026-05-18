from fastapi import status

BASE = "/api/v1/orders"

ORDER_DATA = {
    "user_id": 5,
    "status": "pending",
    "total": "150.00",
}

ORDER_UPDATE = {
    "status": "paid",
}

PAYMENT_DATA = {
    "order_id": 1,
    "payment_method_id": 1,
    "amount": "150.00",
    "status": "pending",
}


class TestCreateOrder:
    def test_crear(self, client):
        response = client.post(BASE + "/", json=ORDER_DATA)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user_id"] == ORDER_DATA["user_id"]
        assert data["status"] == ORDER_DATA["status"]
        assert "id" in data

    def test_crear_datos_invalidos(self, client):
        response = client.post(BASE + "/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_crear_status_invalido(self, client):
        data = {**ORDER_DATA, "status": "invalid_status"}
        response = client.post(BASE + "/", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetOrder:
    def test_obtener(self, client):
        response = client.get(f"{BASE}/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1

    def test_obtener_no_existente(self, client):
        response = client.get(f"{BASE}/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Orden no encontrada" in response.json()["detail"]


class TestListOrders:
    def test_listar(self, client):
        response = client.get(BASE + "/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_listar_por_usuario(self, client):
        response = client.get(f"{BASE}/user/5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestUpdateOrder:
    def test_actualizar(self, client):
        response = client.put(f"{BASE}/1", json=ORDER_UPDATE)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == ORDER_UPDATE["status"]

    def test_actualizar_no_existente(self, client):
        response = client.put(f"{BASE}/999", json=ORDER_UPDATE)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Orden no encontrada" in response.json()["detail"]


class TestDeleteOrder:
    def test_eliminar(self, client):
        response = client.delete(f"{BASE}/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_eliminar_no_existente(self, client):
        response = client.delete(f"{BASE}/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Orden no encontrada" in response.json()["detail"]


class TestOrderPayments:
    def _crear_orden(self, client, user_id=6):
        orden = client.post(BASE + "/", json={**ORDER_DATA, "user_id": user_id})
        return orden.json()["id"]

    def test_crear_pago(self, client):
        order_id = self._crear_orden(client)
        pago = {"order_id": order_id, "payment_method_id": 1, "amount": "150.00", "status": "pending"}
        response = client.post(f"{BASE}/{order_id}/payments/", json=pago)
        assert response.status_code == status.HTTP_201_CREATED, response.text
        data = response.json()
        assert data["order_id"] == order_id
        assert "id" in data

    def test_listar_pagos_por_orden(self, client):
        order_id = self._crear_orden(client, user_id=7)
        pago = {"order_id": order_id, "payment_method_id": 1, "amount": "100.00", "status": "pending"}
        client.post(f"{BASE}/{order_id}/payments/", json=pago)
        response = client.get(f"{BASE}/{order_id}/payments/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_actualizar_pago(self, client):
        order_id = self._crear_orden(client, user_id=8)
        pago = {"order_id": order_id, "payment_method_id": 1, "amount": "200.00", "status": "pending"}
        resp = client.post(f"{BASE}/{order_id}/payments/", json=pago)
        payment_id = resp.json()["id"]
        response = client.put(f"{BASE}/payments/{payment_id}", json={"status": "confirmed"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "confirmed"
