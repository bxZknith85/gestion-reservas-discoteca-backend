import pytest


@pytest.mark.django_db
class TestCreateTable:
    def test_create_table_success(self, auth_client, table_data):
        response = auth_client.post("/api/v1/tables/", table_data, format="json")
        assert response.status_code == 201
        assert response.data["number"] == 1

    def test_create_table_duplicate_number(self, auth_client, table_data, test_table):
        response = auth_client.post("/api/v1/tables/", table_data, format="json")
        assert response.status_code == 400

    def test_create_table_unauthenticated(self, api_client, table_data):
        response = api_client.post("/api/v1/tables/", table_data, format="json")
        assert response.status_code == 401


@pytest.mark.django_db
class TestGetTable:
    def test_get_table(self, auth_client, test_table):
        response = auth_client.get(f"/api/v1/tables/{test_table.id}/")
        assert response.status_code == 200
        assert response.data["number"] == test_table.number

    def test_get_nonexistent_table(self, auth_client):
        response = auth_client.get("/api/v1/tables/99999/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestListTables:
    def test_list_tables(self, auth_client, test_table):
        response = auth_client.get("/api/v1/tables/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestUpdateTable:
    def test_update_table(self, auth_client, test_table):
        response = auth_client.put(
            f"/api/v1/tables/{test_table.id}/",
            {"number": 2, "table_type": 1, "capacity": 6, "table_state": 1},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["number"] == 2


@pytest.mark.django_db
class TestDeleteTable:
    def test_delete_table(self, auth_client, test_table):
        response = auth_client.delete(f"/api/v1/tables/{test_table.id}/")
        assert response.status_code == 204
