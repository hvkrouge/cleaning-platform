# Cleaning Platform MVP

Three applications over one shared FastAPI backend:

- `apps/customer` — customer booking experience
- `apps/partner` — partner availability and job execution
- `apps/admin` — operations control center
- `apps/api` — shared backend

## MVP vertical slice

Customer → quote → slot → booking → admin assignment → partner accepts → job starts/completes → partner earning.

## Local backend smoke test

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
APP_DATABASE_URL=sqlite:///./cleaning.db uvicorn app.main:app --reload --port 8000
```

Open http://127.0.0.1:8000/docs.

For production/local Docker, set `APP_DATABASE_URL` to a PostgreSQL URL.
