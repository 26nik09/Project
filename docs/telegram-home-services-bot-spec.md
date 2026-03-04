# Telegram Home Services Bot — Product & MVP Blueprint

## 1) Product Scope

This document defines an MVP for a Telegram bot where users can order **home service professionals**.

### Core roles
- **Client**: browses profiles, searches/filters, creates service requests, chats with master, leaves reviews.
- **Master**: receives requests, chats with clients, can reply to reviews.
- **Admin**: manages masters/profiles/categories/tags/reviews/users/payments with role-based permissions.

### Constraints confirmed by stakeholder
- Registration/login: Telegram-only.
- Master and Client are separate roles (no dual role for the same account).
- Initial operation: one real master owner + optional placeholder profiles.
- Languages: English default + Hindi switch.
- Geography: India (city/area-first matching).

---

## 2) Why Admin Web Panel vs Admin-Only Telegram Commands

### Option A — Admin in Telegram only
**Pros**
- Fastest to launch.
- No extra front-end.
- Lower infrastructure complexity.

**Cons**
- Hard to manage many profiles/photos/videos and moderation queues.
- Limited table filtering/sorting/bulk editing UX.
- Harder role-based access control for multiple admins.

### Option B — Dedicated Web Admin Panel (recommended)
**Pros**
- Better content management (profiles, media, categories, tags).
- Clear moderation dashboard for reviews.
- Better multi-admin permission model (super admin/moderator/content manager).
- Easier long-term maintenance.

**Cons**
- Slightly longer implementation time.
- Requires minimal web hosting.

**Recommendation**: Build Telegram bot for end users + lightweight web admin panel for operations.

---

## 3) MVP Feature Set

## 3.1 Client-side bot features
1. Onboarding:
   - Language selector (EN/HI).
   - 18+ confirmation checkbox at first start.
2. Home:
   - Recommended masters.
   - Search input.
   - Categories tab.
3. Search and discovery:
   - Partial name matching.
   - Free-text matching against name, services, tags, and description.
   - Mandatory city filter in flow.
   - Sorting: default `newest`, optional price/rating.
   - Pagination (`Prev/Next`).
4. Master profile view:
   - Name/alias, city, district, categories, services, prices, tags.
   - Physical metadata as requested: age, height, weight, shoe size.
   - Special skills field.
   - Availability and online/offline status.
   - Up to 10 media items (photos/videos).
   - Button: `Create Request`.
5. Booking flow:
   - Select date/time/service.
   - Create request.
   - Open in-bot client↔master chat immediately after request creation.
   - Full prepayment flow (phase-by-phase, see Payments).
   - Client can cancel request.
6. Reviews:
   - Only after service is marked delivered.
   - One-way publishing (no edit).
   - Master can reply.

## 3.2 Master-side features (bot)
1. Receive request notifications.
2. In-bot chat with client.
3. Request overview (basic list/history).
4. Reply to reviews.

## 3.3 Admin-side features (web panel)
1. Authentication and roles:
   - Super Admin.
   - Moderator.
   - Content Manager.
2. User management:
   - Ban/unban clients.
3. Master/profile management:
   - Create/edit/publish/hide profiles.
   - Media uploads (max 10 items per profile).
   - Set required fields and pricing mode.
4. Taxonomy management:
   - Categories and tags managed by admin only.
5. Review moderation:
   - Manual approve/reject queue.
6. Payment and order visibility:
   - List and details for operational tracking.

---

## 4) Profile Data Model (MVP)

### Required fields to publish
- `display_name`
- `city`
- `district`
- `categories[]`
- `services[]`
- `price` (hourly and/or fixed)
- `currency`
- `at_least_one_photo`

### Optional/extended fields
- `age` (exact)
- `height_cm`
- `weight_kg`
- `shoe_size`
- `special_skills`
- `tags[]`
- `service_area`
- `availability_schedule`
- `online_status`
- `videos[]`

### Profile limits
- Max media per profile: **10**.

---

## 5) Localization (EN + HI)

1. UI dictionary in two locales:
   - `en`
   - `hi`
2. Language switch available from main menu anytime.
3. Profile text content is translated manually in admin panel (no auto-translation in MVP).

---

## 6) Payments Roadmap

## Phase 1 (MVP practical)
- Support one primary payment channel first (recommend UPI/provider easiest for India launch).
- Mark payments as prepaid and route to owner account.
- Manual reconciliation allowed in admin panel.

## Phase 2
- Telegram Payments where available.
- Card provider integration.
- Crypto payment gateway integration.

> Note: You requested “all at once,” but to reduce launch risk for a solo-maintained product,
> phase rollout is strongly recommended.

---

## 7) Suggested Tech Stack (easy to maintain)

- **Bot**: Python + aiogram
- **Backend/API**: FastAPI
- **DB**: SQLite for MVP (migration path to PostgreSQL)
- **Admin panel**: simple server-rendered FastAPI/Jinja or lightweight React admin
- **ORM**: SQLAlchemy + Alembic migrations
- **Queue/background**: optional APScheduler/Celery later
- **Storage**: local/S3-compatible for profile media

Why this stack:
- Large Python ecosystem.
- Good beginner maintainability.
- Straightforward deployment path.

---

## 8) Minimal Database Schema (MVP)

- `users` (telegram_id, role, language, is_banned, is_adult_confirmed)
- `admin_roles` (user_id, role_type)
- `masters` (user_id/null for placeholder, online_status, profile_status)
- `master_profiles` (master_id, locale, bio, physical fields, city/district, service_area)
- `categories`
- `tags`
- `master_categories`
- `master_tags`
- `services` (master_id, name, description, price_type, price_amount, currency)
- `media_assets` (master_id, type photo/video, url/order)
- `availability_slots`
- `booking_requests` (client_id, master_id, datetime, chosen_service, status)
- `chat_threads`
- `chat_messages`
- `payments` (booking_id, provider, amount, currency, status)
- `reviews` (booking_id, client_id, master_id, rating, text, moderation_status)
- `review_replies`

---

## 9) Bot UX Map (MVP)

## Client
`/start` → choose language → confirm 18+ → Home

Home:
- `Recommended`
- `Search`
- `Categories`
- `My Requests`
- `Language`

Profile:
- View media/info/reviews
- `Create Request`

Request flow:
- Choose service/date/time
- Confirm prepayment
- Open chat with master

After completion:
- Leave review

## Master
- New request alerts
- Request list
- Chat list
- Review replies

## Admin (web)
- Dashboard
- Masters/Profiles
- Categories/Tags
- Reviews moderation
- Users (ban/unban)
- Payments log
- Admin role permissions

---

## 10) Security, Policy, and Operations Notes

1. Add Terms + Privacy links in bot menu.
2. Enforce strict content moderation policy for profile media.
3. Audit log in admin panel for sensitive actions.
4. Rate-limit search and messaging.
5. Validate media upload type/size.

---

## 11) Delivery Plan (2–3 weeks MVP)

### Week 1
- Project scaffolding, DB schema, migrations.
- User onboarding (EN/HI + 18+).
- Admin auth and role model.
- Categories/tags CRUD.

### Week 2
- Master profile CRUD + media.
- Client search/filter/sort/pagination.
- Booking request creation + in-bot chat thread.

### Week 3
- Payment integration (first provider).
- Reviews + moderation + master replies.
- Ban/unban, QA, and deployment prep.

---

## 12) Open Decisions Before Implementation Start

1. First payment provider in India (UPI/aggregator choice).
2. Hosting target (Railway/Render/VPS/etc).
3. Admin panel UI approach (simple templates vs SPA).
4. Exact moderation policy text.
5. Service completion trigger (who marks completed: admin/master/client rule).

