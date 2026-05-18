from fastapi import status

BASE = "/api/v1/users"

USER_DATA = {
    "email": "test@example.com",
    "username": "testuser",
    "phone_number": "1234567890",
    "type_user_id": 1,
    "password": "password123",
}

USER_UPDATE = {
    "phone_number": "0987654321",
    "is_active": False,
}


class TestCreateUser:
    def test_crear_usuario(self, client):
        response = client.post(BASE + "/", json=USER_DATA)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == USER_DATA["email"]
        assert data["username"] == USER_DATA["username"]
        assert data["phone_number"] == USER_DATA["phone_number"]
        assert "id" in data
        assert data["is_active"] is True

    def test_crear_usuario_email_duplicado(self, client):
        response = client.post(BASE + "/", json=USER_DATA)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email ya registrado" in response.json()["detail"]

    def test_crear_usuario_telefono_duplicado(self, client):
        data = {**USER_DATA, "email": "otro@example.com"}
        response = client.post(BASE + "/", json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Teléfono ya registrado" in response.json()["detail"]

    def test_crear_usuario_datos_invalidos(self, client):
        response = client.post(BASE + "/", json={"email": "invalido"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetUser:
    def test_obtener_usuario(self, client):
        response = client.get(f"{BASE}/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["email"] == USER_DATA["email"]

    def test_obtener_usuario_no_existente(self, client):
        response = client.get(f"{BASE}/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Usuario no encontrado" in response.json()["detail"]


class TestListUsers:
    def test_listar_usuarios(self, client):
        response = client.get(BASE + "/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_listar_usuarios_con_paginacion(self, client):
        response = client.get(BASE + "/?skip=0&limit=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestUpdateUser:
    def test_actualizar_usuario(self, client):
        response = client.put(f"{BASE}/1", json=USER_UPDATE)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["phone_number"] == USER_UPDATE["phone_number"]
        assert data["is_active"] == USER_UPDATE["is_active"]

    def test_actualizar_usuario_no_existente(self, client):
        response = client.put(f"{BASE}/999", json=USER_UPDATE)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Usuario no encontrado" in response.json()["detail"]


class TestDeleteUser:
    def test_eliminar_usuario(self, client):
        response = client.delete(f"{BASE}/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_eliminar_usuario_no_existente(self, client):
        response = client.delete(f"{BASE}/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Usuario no encontrado" in response.json()["detail"]
