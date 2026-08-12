# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Website for a ballet school, built with FastAPI (Python 3.12).

## Status

MVP is in place: a FastAPI app under `app/` with server-rendered Jinja2 templates for Home, About, Classes, Contact, and Login/Signup, backed by async SQLAlchemy + SQLite, split into routers with a pytest test suite.

## Environment

- Virtual environment lives in `venv/` — activate with `source venv/bin/activate` before running any Python command.
- Secrets/config belong in `.env` (gitignored) — `SECRET_KEY` is required; the app fails fast with a friendly message if it's missing.
- Install dependencies with `pip install -r requirements.txt`.

## Commands

- Run the dev server: `uvicorn app.main:app --reload`
- Run the test suite: `pytest`
- Lint/format: `ruff check .` / `ruff format .`
- do some commits every time you complete a task worth of commiting

## Code Review

- After implementing or editing any code, invoke the `code-review-subagent` (Agent tool) to review the diff before reporting the task as done. It only reviews changed files/hunks, not the whole codebase.
- Also invoke `code-review-subagent` whenever the user asks for a code review.

## Architecture

- `app/main.py` — FastAPI app factory: lifespan, session middleware, static mount, router includes, 404/500 exception handlers.
- `app/config.py` — Settings loader (`SECRET_KEY`, etc.) with a friendly startup error if required env vars are missing.
- `app/content.py` — static placeholder content: nav links, class schedule, instructors, testimonials, FAQ.
- `app/templating.py` — shared `Jinja2Templates` instance + `render()`/`base_context()` context helpers used by all routers.
- `app/routers/pages.py` — public page routes (`/`, `/about`, `/classes`, `/contact`, `/robots.txt`).
- `app/routers/auth.py` — signup/login/logout routes.
- `app/auth.py`, `app/database.py`, `app/models.py` — password hashing/session helpers, async SQLAlchemy engine/session setup, `User` model.
- `app/templates/` — Jinja2 templates: `base.html` layout, `partials/` (nav, footer), `errors/` (404, 500), one template per page.
- `app/static/` — CSS, JS, images, favicon, `robots.txt`, served at `/static` (`robots.txt` also exposed at `/robots.txt`).
- `app/tests/` — pytest suite (`httpx.AsyncClient` against the ASGI app, in-memory SQLite via a `get_db` dependency override).
