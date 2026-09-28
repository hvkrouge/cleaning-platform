api-install:
	cd apps/api && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

api-seed:
	cd apps/api && APP_DATABASE_URL=sqlite:///./cleaning.db PYTHONPATH=. python3 -m app.seed

api-dev:
	cd apps/api && APP_DATABASE_URL=sqlite:///./cleaning.db PYTHONPATH=. uvicorn app.main:app --reload --port 8000

docker-up:
	docker compose up -d
