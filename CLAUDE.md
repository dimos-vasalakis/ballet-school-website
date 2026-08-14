# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Website for a ballet school, built with FastAPI (Python 3.12).

## Status

Production-hardened: a FastAPI app under `app/` with server-rendered Jinja2 templates for Home, About, Classes, Contact, and Login/Signup, backed by async SQLAlchemy + Postgres, split into routers with a pytest test suite. CSRF protection, rate limiting, security headers, structured logging, a health check, and Alembic migrations are in place; deployable via Docker.

## Environment

- Virtual environment lives in `venv/` — activate with `source venv/bin/activate` before running any Python command.
- Secrets/config belong in `.env` (gitignored) — `SECRET_KEY` is required; the app fails fast with a friendly message if it's missing. `ENVIRONMENT` (`development`/`production`) and `DATABASE_URL` are optional with sane dev defaults.
- Install dependencies with `pip install -r requirements-dev.txt` for local dev/test (runtime-only deps live in `requirements.txt`, used by the Dockerfile).
- Requires a local Postgres instance (or `docker compose up db`) — see `.env.example` for the default `DATABASE_URL`.

## Commands

- Run the dev server: `uvicorn app.main:app --reload`
- Run the test suite: `pytest`
- Lint/format: `ruff check .` / `ruff format .`
- Apply DB migrations: `alembic upgrade head`
- Create a migration after changing `app/models.py`: `alembic revision --autogenerate -m "..."`
- do some commits every time you complete a task worth of commiting

## Code Review

- After implementing or editing any code, invoke the `code-review-subagent` (Agent tool) to review the diff before reporting the task as done. It only reviews changed files/hunks, not the whole codebase.
- Also invoke `code-review-subagent` whenever the user asks for a code review.

## Architecture

- `app/main.py` — FastAPI app factory: lifespan, logging setup, rate limiter, security headers + session middleware, static mount, router includes, 404/500 exception handlers (500s are logged server-side).
- `app/config.py` — Settings loader (`SECRET_KEY`, `ENVIRONMENT`, `DATABASE_URL`) with a friendly startup error if `SECRET_KEY` is missing.
- `app/content.py` — static placeholder content: nav links, class schedule, instructors, testimonials, FAQ.
- `app/templating.py` — shared `Jinja2Templates` instance + `render()`/`base_context()` context helpers used by all routers; `base_context()` also injects a per-session CSRF token.
- `app/csrf.py` — CSRF token generation (`get_csrf_token`) and verification dependency (`verify_csrf`); every POST form must include a `csrf_token` hidden field and every POST route must depend on `verify_csrf`.
- `app/rate_limit.py` — shared `slowapi` `Limiter` instance (imported by `main.py` and `routers/auth.py` to avoid a circular import).
- `app/middleware.py` — `SecurityHeadersMiddleware` (X-Content-Type-Options, X-Frame-Options, Referrer-Policy, HSTS in production).
- `app/logging_config.py` — stdlib logging setup, level gated by `ENVIRONMENT`.
- `app/routers/pages.py` — public page routes (`/`, `/about`, `/classes`, `/contact`, `/robots.txt`).
- `app/routers/auth.py` — signup/login/logout routes (rate-limited, CSRF-protected).
- `app/routers/health.py` — `/healthz` liveness endpoint.
- `app/auth.py`, `app/database.py`, `app/models.py` — password hashing/session helpers, async SQLAlchemy engine/session setup (Postgres via `DATABASE_URL`), `User` model.
- `alembic/`, `alembic.ini` — DB migrations; schema is no longer created via `create_all`, only via `alembic upgrade head`.
- `app/templates/` — Jinja2 templates: `base.html` layout, `partials/` (nav, footer), `errors/` (404, 500), one template per page.
- `app/static/` — CSS, JS, images, favicon, `robots.txt`, served at `/static` (`robots.txt` also exposed at `/robots.txt`).
- `app/tests/` — pytest suite (`httpx.AsyncClient` against the ASGI app, in-memory SQLite via a `get_db` dependency override); `conftest.py`'s `get_csrf_token()` helper fetches a valid CSRF token for POST tests, and the `client` fixture resets the rate limiter between tests.
- `Dockerfile`, `docker-compose.yml` — single-instance production image (gunicorn + 1 uvicorn worker, runs `alembic upgrade head` on start) plus a local Postgres service.
- `.github/workflows/ci.yml` — runs `ruff check`, `ruff format --check`, and `pytest` on push/PR.
