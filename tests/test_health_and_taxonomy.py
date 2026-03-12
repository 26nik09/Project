from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_create_and_list_category() -> None:
    headers = {"X-Admin-Token": "change-me"}
    with TestClient(app) as client:
        create_response = client.post(
            "/taxonomy/categories",
            json={
                "slug": "plumber",
                "name_en": "Plumber",
                "name_hi": "प्लम्बर",
                "description": "Water and pipe repair",
            },
            headers=headers,
        )
        assert create_response.status_code in (201, 409)

        list_response = client.get("/taxonomy/categories")
        assert list_response.status_code == 200
        data = list_response.json()
        assert any(item["slug"] == "plumber" for item in data)
