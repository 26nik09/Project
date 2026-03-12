from fastapi.testclient import TestClient

from app.main import app


def test_admin_create_master_and_catalog_search() -> None:
    headers = {"X-Admin-Token": "change-me"}

    with TestClient(app) as client:
        category_response = client.post(
            "/taxonomy/categories",
            json={
                "slug": "electrician",
                "name_en": "Electrician",
                "name_hi": "इलेक्ट्रीशियन",
                "description": "Electrical works",
            },
            headers=headers,
        )
        assert category_response.status_code in (201, 409)

        categories = client.get("/taxonomy/categories").json()
        electrician_id = next(item["id"] for item in categories if item["slug"] == "electrician")

        create_master = client.post(
            "/admin/masters",
            json={
                "display_name": "Rahul Fix",
                "city": "Delhi",
                "district": "South Delhi",
                "bio": "Home electrician and wiring specialist",
                "online_status": True,
                "category_ids": [electrician_id],
                "services": [
                    {
                        "name": "Fan Repair",
                        "description": "Repair and install ceiling fans",
                        "price_amount": 500,
                        "currency": "INR",
                    }
                ],
            },
            headers=headers,
        )
        assert create_master.status_code == 201
        master = create_master.json()

        search = client.get("/catalog/masters", params={"q": "rahul", "city": "Delhi"})
        assert search.status_code == 200
        masters = search.json()
        assert any(item["id"] == master["id"] for item in masters)

        details = client.get(f"/catalog/masters/{master['id']}")
        assert details.status_code == 200
        payload = details.json()
        assert payload["display_name"] == "Rahul Fix"
        assert payload["services"][0]["name"] == "Fan Repair"
