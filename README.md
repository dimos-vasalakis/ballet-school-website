# Ballet School Website

A website for a ballet school, built with [FastAPI](https://fastapi.tiangolo.com/).

## Status

MVP complete — Home, About, Classes, Contact, and Login/Signup pages, server-rendered with Jinja2 and backed by async SQLAlchemy + Postgres. Hardened for production: CSRF protection, rate-limited auth, security headers, structured logging, health check, and Alembic migrations.

## Getting Started

### Prerequisites

- Python 3.12+
- A local Postgres instance (or `docker compose up db`)

### Setup

```bash
# Activate the virtual environment
source venv/bin/activate

# Install dependencies (includes dev/test tooling)
pip install -r requirements-dev.txt
```

### Environment Variables

Copy `.env.example` to `.env` and set `SECRET_KEY` (used to sign session cookies) and `DATABASE_URL`:

```bash
cp .env.example .env
python3 -c "import secrets; print(secrets.token_hex(32))"  # paste the output as SECRET_KEY
```

### Database

Run migrations before starting the app for the first time, and any time `app/models.py` changes:

```bash
alembic upgrade head
```

To create a new migration after changing `app/models.py`:

```bash
alembic revision --autogenerate -m "describe the change"
```

### Running the app

```bash
uvicorn app.main:app --reload
```

Then visit http://127.0.0.1:8000

### Running the tests

```bash
pytest
```

## Production Deployment

The app is sized for a **single-instance** deployment (in-memory rate limiting and startup-time migrations both assume one running container).

### Via Docker Compose

```bash
cp .env.example .env   # set a real SECRET_KEY, leave DATABASE_URL as-is (points at the db service)
docker compose up --build
```

This brings up the app (gunicorn + 1 uvicorn worker) and a Postgres 16 database with a persistent volume. Migrations run automatically on container start.

### Required environment variables

- `SECRET_KEY` — required, no default.
- `ENVIRONMENT=production` — enables secure session cookies (`Secure` flag) and HSTS.
- `DATABASE_URL` — e.g. `postgresql+asyncpg://user:pass@host:5432/dbname`.

### Without Docker

```bash
alembic upgrade head
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:8000
```

### Health check

`GET /healthz` returns `{"status": "ok"}` — use it for a load balancer/platform liveness probe.
