import pytest


@pytest.mark.django_db
class TestCreateOrderDetail:
    def test_create_success(self, auth_client, test_user):
        from apps.transactions.models import Order
        order = Order.objects.create(user=test_user, total="0")
        data = {"order": order.id, "quantity": 2, "unit_price": "25000.00", "discount": "0.00"}
        response = auth_client.post("/api/v1/order-details/", data, format="json")
        assert response.status_code == 201

    def test_create_unauthenticated(self, api_client, test_user):
        from apps.transactions.models import Order
        order = Order.objects.create(user=test_user, total="0")
        data = {"order": order.id, "quantity": 1, "unit_price": "50000.00", "discount": "0.00"}
        response = api_client.post("/api/v1/order-details/", data, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestGetOrderDetail:
    def test_get(self, auth_client, test_user):
        from apps.transactions.models import Order, OrderDetail
        order = Order.objects.create(user=test_user, total="0")
        od = OrderDetail.objects.create(order=order, quantity=1, unit_price="50000", discount="0")
        response = auth_client.get(f"/api/v1/order-details/{od.id}/")
        assert response.status_code == 200

    def test_get_nonexistent(self, auth_client):
        response = auth_client.get("/api/v1/order-details/99999/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestListOrderDetails:
    def test_list(self, auth_client, test_user):
        from apps.transactions.models import Order, OrderDetail
        order = Order.objects.create(user=test_user, total="0")
        OrderDetail.objects.create(order=order, quantity=1, unit_price="50000", discount="0")
        response = auth_client.get("/api/v1/order-details/")
        assert response.status_code == 200

    def test_list_by_order(self, auth_client, test_user):
        from apps.transactions.models import Order, OrderDetail
        order = Order.objects.create(user=test_user, total="0")
        OrderDetail.objects.create(order=order, quantity=1, unit_price="50000", discount="0")
        response = auth_client.get(f"/api/v1/order-details/?order={order.id}")
        assert response.status_code == 200


@pytest.mark.django_db
class TestUpdateOrderDetail:
    def test_update(self, auth_client, test_user):
        from apps.transactions.models import Order, OrderDetail
        order = Order.objects.create(user=test_user, total="0")
        od = OrderDetail.objects.create(order=order, quantity=1, unit_price="50000", discount="0")
        response = auth_client.put(
            f"/api/v1/order-details/{od.id}/",
            {"order": order.id, "quantity": 3, "unit_price": "45000.00", "discount": "5000.00"},
            format="json",
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestDeleteOrderDetail:
    def test_delete(self, auth_client, test_user):
        from apps.transactions.models import Order, OrderDetail
        order = Order.objects.create(user=test_user, total="0")
        od = OrderDetail.objects.create(order=order, quantity=1, unit_price="50000", discount="0")
        response = auth_client.delete(f"/api/v1/order-details/{od.id}/")
        assert response.status_code == 204
