# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Website for a ballet school, built with FastAPI (Python 3.12).

## Status

MVP is in place: a FastAPI app under `app/` with server-rendered Jinja2 templates for Home, About, Classes, and Contact (with a working POST handler), plus static CSS/JS.

## Environment

- Virtual environment lives in `venv/` — activate with `source venv/bin/activate` before running any Python command.
- Secrets/config belong in `.env` (gitignored).
- Install dependencies with `pip install -r requirements.txt`.

## Commands

- Run the dev server: `uvicorn app.main:app --reload`
- do some commits every time you complete a task worth of commiting

## Code Review

- After implementing or editing any code, invoke the `code-review-subagent` (Agent tool) to review the diff before reporting the task as done. It only reviews changed files/hunks, not the whole codebase.
- Also invoke `code-review-subagent` whenever the user asks for a code review.

## Architecture

- `app/main.py` — FastAPI app, route handlers, in-memory `NAV_LINKS`/`CLASSES` data.
- `app/templates/` — Jinja2 templates (`base.html` layout + one per page).
- `app/static/` — CSS and JS assets served at `/static`.
