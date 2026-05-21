import pytest


@pytest.mark.django_db
class TestHealth:
    def test_root_health(self, api_client):
        response = api_client.get("/health/")
        assert response.status_code == 200
        assert response.data["status"] == "ok"

    def test_api_health(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert response.status_code == 200
        assert response.data["status"] == "ok"
