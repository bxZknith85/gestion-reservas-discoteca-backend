import pytest


@pytest.mark.django_db
class TestCreateTablePrice:
    def test_create_success(self, auth_client, test_table, test_event):
        data = {"table": test_table.id, "event": test_event.id, "price": "150000.00"}
        response = auth_client.post("/api/v1/table-prices/", data, format="json")
        assert response.status_code == 201

    def test_create_duplicate(self, auth_client, test_table, test_event):
        from apps.core.models import TablePrice
        TablePrice.objects.create(table=test_table, event=test_event, price="150000")
        data = {"table": test_table.id, "event": test_event.id, "price": "200000.00"}
        response = auth_client.post("/api/v1/table-prices/", data, format="json")
        assert response.status_code == 400

    def test_create_unauthenticated(self, api_client, test_table, test_event):
        data = {"table": test_table.id, "event": test_event.id, "price": "150000.00"}
        response = api_client.post("/api/v1/table-prices/", data, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestGetTablePrice:
    def test_get(self, auth_client, test_table, test_event):
        from apps.core.models import TablePrice
        tp = TablePrice.objects.create(table=test_table, event=test_event, price="150000")
        response = auth_client.get(f"/api/v1/table-prices/{tp.id}/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestListTablePrices:
    def test_list(self, auth_client, test_table, test_event):
        from apps.core.models import TablePrice
        TablePrice.objects.create(table=test_table, event=test_event, price="150000")
        response = auth_client.get("/api/v1/table-prices/")
        assert response.status_code == 200

    def test_list_by_event(self, auth_client, test_table, test_event):
        from apps.core.models import TablePrice
        TablePrice.objects.create(table=test_table, event=test_event, price="150000")
        response = auth_client.get(f"/api/v1/table-prices/?event={test_event.id}")
        assert response.status_code == 200

    def test_list_by_table(self, auth_client, test_table, test_event):
        from apps.core.models import TablePrice
        TablePrice.objects.create(table=test_table, event=test_event, price="150000")
        response = auth_client.get(f"/api/v1/table-prices/?table={test_table.id}")
        assert response.status_code == 200


@pytest.mark.django_db
class TestUpdateTablePrice:
    def test_update(self, auth_client, test_table, test_event):
        from apps.core.models import TablePrice
        tp = TablePrice.objects.create(table=test_table, event=test_event, price="150000")
        response = auth_client.put(
            f"/api/v1/table-prices/{tp.id}/",
            {"table": test_table.id, "event": test_event.id, "price": "200000.00"},
            format="json",
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestDeleteTablePrice:
    def test_delete(self, auth_client, test_table, test_event):
        from apps.core.models import TablePrice
        tp = TablePrice.objects.create(table=test_table, event=test_event, price="150000")
        response = auth_client.delete(f"/api/v1/table-prices/{tp.id}/")
        assert response.status_code == 204
