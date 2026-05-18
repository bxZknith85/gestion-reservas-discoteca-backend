from fastapi import status

from app.core.security import create_access_token, decode_access_token

BASE = "/api/v1/auth"

USER_DATA = {
    "email": "auth@test.com",
    "username": "authtest",
    "phone_number": "1112223333",
    "type_user_id": 1,
    "password": "securepass123",
}


class TestLogin:
    def test_login_exitoso(self, client):
        client.post("/api/v1/users/", json=USER_DATA)
        response = client.post(
            f"{BASE}/login",
            json={"email": USER_DATA["email"], "password": USER_DATA["password"]},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["email"] == USER_DATA["email"]
        assert data["username"] == USER_DATA["username"]
        assert data["user_id"] > 0

        payload = decode_access_token(data["access_token"])
        assert payload is not None
        assert payload["sub"] == str(data["user_id"])

    def test_login_email_incorrecto(self, client):
        response = client.post(
            f"{BASE}/login",
            json={"email": "noexiste@test.com", "password": "cualquiera"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Credenciales inválidas"

    def test_login_password_incorrecto(self, client):
        client.post("/api/v1/users/", json={**USER_DATA, "email": "passfail@test.com"})
        response = client.post(
            f"{BASE}/login",
            json={"email": "passfail@test.com", "password": "wrongpassword"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_datos_invalidos(self, client):
        response = client.post(f"{BASE}/login", json={"email": "invalido"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetCurrentUser:
    def test_token_valido(self, client):
        data_usuario = {**USER_DATA, "email": "current@test.com", "phone_number": "4445556666"}
        r_create = client.post("/api/v1/users/", json=data_usuario)
        assert r_create.status_code == 201, r_create.text
        r = client.post(
            f"{BASE}/login",
            json={"email": "current@test.com", "password": USER_DATA["password"]},
        )
        assert r.status_code == 200, r.text
        token = r.json()["access_token"]

        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == "current@test.com"

    def test_token_invalido(self, client):
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer token-invalido"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token inválido" in response.json()["detail"]

    def test_sin_token(self, client):
        response = client.get("/api/v1/users/me")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_token_expirado(self, client):
        from datetime import timedelta

        token = create_access_token({"sub": "1"}, expires_delta=timedelta(seconds=-1))
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
