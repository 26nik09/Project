# Home Services Telegram Bot — Week 1 Scaffold

This repository now contains the Week 1 implementation baseline from the MVP plan:

- FastAPI backend scaffold.
- SQLite-backed SQLAlchemy models for users/admin roles/categories/tags.
- Admin-protected CRUD endpoints for categories and tags.
- Basic admin user/role APIs.
- Aiogram onboarding flow with language selection (EN/HI) and 18+ confirmation.
- Initial SQL migration script.

## Run backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

## Run bot

```bash
export BOT_TOKEN="<your-telegram-bot-token>"
python -m app.bot.run
```

## Admin API authentication

Set `ADMIN_TOKEN` in `.env` (defaults to `change-me`).
Set `WEBAPP_URL` in `.env` (defaults to `http://localhost:8000/webapp`).

Send header:

```text
X-Admin-Token: <token>
```

## Next steps (Week 2)

- Master profile CRUD with media (max 10 assets).
- Search/filter/sort/pagination over profiles.
- Booking request creation and chat thread persistence.

## Notes

- The app uses FastAPI lifespan startup instead of deprecated `@app.on_event("startup")`, so you should not see that deprecation warning in current code.


## Telegram WebApp

- Open `http://localhost:8000/webapp` in browser for local preview.
- In Telegram, after onboarding, press **Open Web App** button.


## Stage 1 (WebApp) breakdown

1. Catalog data layer: master profiles, categories link, services.
2. Public catalog API: list/search/filter/sort + profile details.
3. WebApp UI update: search by text/city and render master cards from `/catalog/masters`.


## Stage 2 (WebApp) breakdown

1. Booking backend model + migration (`booking_requests`).
2. Booking API: create, list by client Telegram ID, cancel request.
3. WebApp booking form: choose master and submit date/time/service request.
