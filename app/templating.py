from datetime import UTC, datetime
from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.content import NAV_LINKS
from app.core.csrf import get_csrf_token
from app.core.security import get_current_user

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=BASE_DIR / "templates")


def current_year() -> int:
    return datetime.now(UTC).year


def base_context(request: Request, active: str | None = None, current_user=None) -> dict:
    return {
        "request": request,
        "nav_links": NAV_LINKS,
        "active": active,
        "current_user": current_user,
        "current_year": current_year(),
        "csrf_token": get_csrf_token(request),
    }


async def render(
    request: Request,
    db: AsyncSession,
    template_name: str,
    active: str,
    status_code: int = 200,
    **extra,
) -> HTMLResponse:
    current_user = await get_current_user(request, db)
    context = {**base_context(request, active, current_user), **extra}
    return templates.TemplateResponse(template_name, context, status_code=status_code)
