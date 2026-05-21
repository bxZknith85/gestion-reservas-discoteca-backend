import pytest


@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, api_client, user_data, test_user):
        response = api_client.post("/api/v1/auth/login/", {
            "email": user_data["email"],
            "password": user_data["password"],
        })
        assert response.status_code == 200
        assert "access_token" in response.data
        assert "refresh_token" in response.data
        assert response.data["email"] == user_data["email"]

    def test_login_invalid_password(self, api_client, user_data, test_user):
        response = api_client.post("/api/v1/auth/login/", {
            "email": user_data["email"],
            "password": "wrongpass",
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, api_client):
        response = api_client.post("/api/v1/auth/login/", {
            "email": "no@exists.com",
            "password": "testpass123",
        })
        assert response.status_code == 401

    def test_login_missing_fields(self, api_client):
        response = api_client.post("/api/v1/auth/login/", {"email": "test@test.com"})
        assert response.status_code == 400


@pytest.mark.django_db
class TestGetCurrentUser:
    def test_get_me(self, auth_client, test_user):
        response = auth_client.get("/api/v1/users/me/")
        assert response.status_code == 200
        assert response.data["email"] == test_user.email

    def test_get_me_unauthenticated(self, api_client):
        response = api_client.get("/api/v1/users/me/")
        assert response.status_code == 401

    def test_invalid_token(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")
        response = api_client.get("/api/v1/users/me/")
        assert response.status_code == 401
