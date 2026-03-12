from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app


def test_create_and_cancel_booking() -> None:
    headers = {"X-Admin-Token": "change-me"}

    with TestClient(app) as client:
        category_response = client.post(
            "/taxonomy/categories",
            json={
                "slug": "plumber",
                "name_en": "Plumber",
                "name_hi": "प्लम्बर",
                "description": "Pipe fixes",
            },
            headers=headers,
        )
        assert category_response.status_code in (201, 409)

        categories = client.get("/taxonomy/categories").json()
        category_id = next(item["id"] for item in categories if item["slug"] == "plumber")

        create_master = client.post(
            "/admin/masters",
            json={
                "display_name": "Arjun Services",
                "city": "Delhi",
                "district": "West Delhi",
                "bio": "Fast plumbing help",
                "online_status": True,
                "category_ids": [category_id],
                "services": [
                    {
                        "name": "Leak Repair",
                        "description": "Kitchen and bathroom",
                        "price_amount": 700,
                        "currency": "INR",
                    }
                ],
            },
            headers=headers,
        )
        assert create_master.status_code == 201
        master_id = create_master.json()["id"]

        scheduled = datetime.now(tz=timezone.utc) + timedelta(days=1)
        booking = client.post(
            "/bookings",
            json={
                "client_telegram_id": 999111,
                "master_id": master_id,
                "service_name": "Leak Repair",
                "scheduled_for": scheduled.isoformat(),
                "notes": "Need evening slot",
            },
        )
        assert booking.status_code == 201
        booking_payload = booking.json()
        assert booking_payload["status"] == "new"

        by_client = client.get("/bookings/by-client/999111")
        assert by_client.status_code == 200
        rows = by_client.json()
        assert any(item["id"] == booking_payload["id"] for item in rows)

        canceled = client.post(f"/bookings/{booking_payload['id']}/cancel")
        assert canceled.status_code == 200
        assert canceled.json()["status"] == "canceled"
