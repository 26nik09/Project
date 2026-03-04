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

Send header:

```text
X-Admin-Token: <token>
```

## Next steps (Week 2)

- Master profile CRUD with media (max 10 assets).
- Search/filter/sort/pagination over profiles.
- Booking request creation and chat thread persistence.
