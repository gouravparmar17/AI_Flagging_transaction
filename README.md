# AI Flagging Transaction System

Production-ready Django + DRF backend with ML-powered suspicious transaction detection integrated with the existing `Frontend/` static pages.

## Structure

- `Backend/` Django backend (auth, transactions, fraud prediction, dashboard, reports, alerts)
- `Frontend/` existing HTML/CSS/JS frontend + `api.js` API helper

## Setup

```bash
cd Backend
cp .env.example .env
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py train_fraud_model
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/api`

## Implemented APIs

- Auth: `/api/auth/register/`, `/login/`, `/logout/`, `/refresh/`, `/reset-password/`, `/me/`
- Transactions: `/api/transactions/`, `/api/transactions/{id}/`
- Fraud: `/api/fraud/predict/`, `/api/fraud/predictions/`, `/api/fraud/predictions/{id}/`
- Dashboard: `/api/dashboard/summary/`, `/analytics/`, `/charts/`, `/recent-alerts/`
- Reports: `/api/reports/pdf/`, `/excel/`, `/csv/`
- Alerts: `/api/alerts/`, `/api/alerts/{id}/`

## Security

- JWT auth (access + refresh)
- Password hashing via Django auth
- CORS and CSRF trusted origins via environment variables
- API throttling (rate limiting)
- User-level data isolation (`request.user` filtering)

## Supabase PostgreSQL

Set these in `.env`:

- `SUPABASE_DB_NAME`
- `SUPABASE_DB_USER`
- `SUPABASE_DB_PASSWORD`
- `SUPABASE_DB_HOST`
- `SUPABASE_DB_PORT`

If unset, SQLite is used locally.

## Docker

```bash
cd Backend
docker compose up --build
```
