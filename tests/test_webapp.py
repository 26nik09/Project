from fastapi.testclient import TestClient

from app.main import app


def test_webapp_page_exists() -> None:
    with TestClient(app) as client:
        response = client.get('/webapp')
        assert response.status_code == 200
        assert 'Telegram WebApp' in response.text
        assert 'Home Services' in response.text
