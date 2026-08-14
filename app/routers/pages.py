from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.content import CLASSES, FAQ_ITEMS, INSTRUCTORS, TESTIMONIALS
from app.csrf import verify_csrf
from app.database import get_db
from app.templating import render

BASE_DIR = Path(__file__).resolve().parent.parent

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    return await render(request, db, "index.html", "/")


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, db: AsyncSession = Depends(get_db)):
    return await render(
        request,
        db,
        "about.html",
        "/about",
        instructors=INSTRUCTORS,
        testimonials=TESTIMONIALS,
    )


@router.get("/classes", response_class=HTMLResponse)
async def classes(request: Request, db: AsyncSession = Depends(get_db)):
    return await render(
        request, db, "classes.html", "/classes", classes=CLASSES, faq_items=FAQ_ITEMS
    )


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request, db: AsyncSession = Depends(get_db)):
    return await render(request, db, "contact.html", "/contact")


@router.post("/contact", response_class=HTMLResponse, dependencies=[Depends(verify_csrf)])
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    return await render(request, db, "contact.html", "/contact", submitted=True, name=name)


@router.get("/robots.txt", include_in_schema=False)
async def robots_txt():
    return FileResponse(BASE_DIR / "static" / "robots.txt")
