# Ballet School Website

A website for a ballet school, built with [FastAPI](https://fastapi.tiangolo.com/).

## Status

MVP complete — Home, About, Classes, Contact, and Login/Signup pages, server-rendered with Jinja2 and backed by async SQLAlchemy + SQLite.

## Getting Started

### Prerequisites

- Python 3.12+

### Setup

```bash
# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Copy `.env.example` to `.env` and set `SECRET_KEY` (used to sign session cookies):

```bash
cp .env.example .env
python3 -c "import secrets; print(secrets.token_hex(32))"  # paste the output as SECRET_KEY
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
