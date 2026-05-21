import pytest


@pytest.mark.django_db
class TestCreateOrder:
    def test_create_success(self, auth_client, test_user):
        data = {"user": test_user.id, "total": "0.00", "status": "pending"}
        response = auth_client.post("/api/v1/orders/", data, format="json")
        assert response.status_code == 201

    def test_create_with_notes(self, auth_client, test_user):
        data = {"user": test_user.id, "total": "50000.00", "status": "pending", "notes": "Nota de prueba"}
        response = auth_client.post("/api/v1/orders/", data, format="json")
        assert response.status_code == 201

    def test_create_unauthenticated(self, api_client, test_user):
        data = {"user": test_user.id, "total": "0.00"}
        response = api_client.post("/api/v1/orders/", data, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestGetOrder:
    def test_get(self, auth_client, test_user):
        from apps.transactions.models import Order
        order = Order.objects.create(user=test_user, total="50000")
        response = auth_client.get(f"/api/v1/orders/{order.id}/")
        assert response.status_code == 200

    def test_get_nonexistent(self, auth_client):
        response = auth_client.get("/api/v1/orders/99999/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestListOrders:
    def test_list(self, auth_client, test_user):
        from apps.transactions.models import Order
        Order.objects.create(user=test_user, total="50000")
        response = auth_client.get("/api/v1/orders/")
        assert response.status_code == 200

    def test_list_by_user(self, auth_client, test_user):
        from apps.transactions.models import Order
        Order.objects.create(user=test_user, total="50000")
        response = auth_client.get(f"/api/v1/orders/?user={test_user.id}")
        assert response.status_code == 200


@pytest.mark.django_db
class TestUpdateOrder:
    def test_update(self, auth_client, test_user):
        from apps.transactions.models import Order
        order = Order.objects.create(user=test_user, total="50000")
        response = auth_client.put(
            f"/api/v1/orders/{order.id}/",
            {"user": test_user.id, "status": "paid", "total": "50000.00"},
            format="json",
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestDeleteOrder:
    def test_delete(self, auth_client, test_user):
        from apps.transactions.models import Order
        order = Order.objects.create(user=test_user, total="50000")
        response = auth_client.delete(f"/api/v1/orders/{order.id}/")
        assert response.status_code == 204


@pytest.mark.django_db
class TestOrderPayments:
    def test_create_payment(self, auth_client, test_user):
        from apps.transactions.models import Order
        order = Order.objects.create(user=test_user, total="50000")
        data = {"order": order.id, "payment_method": 1, "amount": "50000.00", "status": "pending"}
        response = auth_client.post(f"/api/v1/orders/{order.id}/payments/", data, format="json")
        assert response.status_code == 201

    def test_list_payments(self, auth_client, test_user):
        from apps.transactions.models import Order, Payment
        order = Order.objects.create(user=test_user, total="50000")
        Payment.objects.create(order=order, payment_method_id=1, amount="50000")
        response = auth_client.get(f"/api/v1/orders/{order.id}/payments/")
        assert response.status_code == 200

    def test_update_payment(self, auth_client, test_user):
        from apps.transactions.models import Order, Payment
        order = Order.objects.create(user=test_user, total="50000")
        payment = Payment.objects.create(order=order, payment_method_id=1, amount="50000")
        response = auth_client.put(
            f"/api/v1/payments/{payment.id}/",
            {"order": order.id, "payment_method": 2, "amount": "50000.00", "status": "confirmed"},
            format="json",
        )
        assert response.status_code == 200
