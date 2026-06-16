# Database Migration Guide

## Local SQLite

```bash
cd Backend
python manage.py makemigrations
python manage.py migrate
```

## Supabase PostgreSQL

1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Fill all `SUPABASE_DB_*` values.
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create admin (optional):
   ```bash
   python manage.py createsuperuser
   ```

## Notes

- All data models are migration-managed in Django.
- Model artifacts are generated via `python manage.py train_fraud_model`.
