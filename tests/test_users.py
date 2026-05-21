import pytest


@pytest.mark.django_db
class TestCreateUser:
    def test_create_user_success(self, api_client, user_data):
        response = api_client.post("/api/v1/users/", user_data)
        assert response.status_code == 201
        assert response.data["email"] == user_data["email"]
        assert "password" not in response.data

    def test_create_user_duplicate_email(self, api_client, user_data, test_user):
        response = api_client.post("/api/v1/users/", user_data)
        assert response.status_code == 400

    def test_create_user_missing_fields(self, api_client):
        response = api_client.post("/api/v1/users/", {"email": "test@test.com"})
        assert response.status_code == 400

    def test_create_user_short_password(self, api_client, user_data):
        user_data["password"] = "short"
        response = api_client.post("/api/v1/users/", user_data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestGetUser:
    def test_get_user_by_id(self, auth_client, test_user):
        response = auth_client.get(f"/api/v1/users/{test_user.id}/")
        assert response.status_code == 200
        assert response.data["email"] == test_user.email

    def test_get_nonexistent_user(self, auth_client):
        response = auth_client.get("/api/v1/users/99999/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestListUsers:
    def test_list_users(self, auth_client, test_user):
        response = auth_client.get("/api/v1/users/")
        assert response.status_code == 200
        assert len(response.data["results"]) >= 1

    def test_list_users_unauthenticated(self, api_client):
        response = api_client.get("/api/v1/users/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestUpdateUser:
    def test_update_user(self, auth_client, test_user):
        response = auth_client.put(
            f"/api/v1/users/{test_user.id}/",
            {"phone_number": "3109876543", "email": "test@example.com", "username": "testuser"},
            format="json",
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestDeleteUser:
    def test_delete_user(self, auth_client, test_user):
        response = auth_client.delete(f"/api/v1/users/{test_user.id}/")
        assert response.status_code == 204
