from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from app.auth import get_current_user
from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.routers import auth as auth_router
from app.routers import pages
from app.templating import base_context, templates

BASE_DIR = Path(__file__).resolve().parent

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_title, lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(pages.router)
app.include_router(auth_router.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        async with SessionLocal() as db:
            current_user = await get_current_user(request, db)
        context = base_context(request, current_user=current_user)
        return templates.TemplateResponse("errors/404.html", context, status_code=404)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code, headers=exc.headers)


@app.exception_handler(Exception)
async def server_error_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("errors/500.html", base_context(request), status_code=500)
