# Ballet School Website

A website for a ballet school, built with [FastAPI](https://fastapi.tiangolo.com/).

## Status

MVP complete — Home, About, Classes, and Contact pages, served via server-rendered Jinja2 templates.

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

Copy `.env` and fill in the required values (none defined yet).

### Running the app

```bash
uvicorn app.main:app --reload
```

Then visit http://127.0.0.1:8000
