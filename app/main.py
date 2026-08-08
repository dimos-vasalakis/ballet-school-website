from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Étoile Ballet School")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

NAV_LINKS = [
    {"name": "Home", "path": "/"},
    {"name": "About", "path": "/about"},
    {"name": "Classes", "path": "/classes"},
    {"name": "Contact", "path": "/contact"},
]

CLASSES = [
    {"name": "Pre-Ballet", "ages": "4-6", "day": "Mon & Wed", "time": "4:00 - 4:45 PM"},
    {"name": "Ballet I", "ages": "7-9", "day": "Tue & Thu", "time": "4:00 - 5:00 PM"},
    {"name": "Ballet II", "ages": "10-12", "day": "Tue & Thu", "time": "5:00 - 6:15 PM"},
    {"name": "Intermediate", "ages": "13-15", "day": "Mon & Wed", "time": "5:00 - 6:30 PM"},
    {"name": "Advanced / Pointe", "ages": "16+", "day": "Fri", "time": "5:00 - 7:00 PM"},
    {"name": "Adult Ballet", "ages": "18+", "day": "Sat", "time": "10:00 - 11:15 AM"},
]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "nav_links": NAV_LINKS, "active": "/"}
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        "about.html", {"request": request, "nav_links": NAV_LINKS, "active": "/about"}
    )


@app.get("/classes", response_class=HTMLResponse)
async def classes(request: Request):
    return templates.TemplateResponse(
        "classes.html",
        {"request": request, "nav_links": NAV_LINKS, "active": "/classes", "classes": CLASSES},
    )


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(
        "contact.html", {"request": request, "nav_links": NAV_LINKS, "active": "/contact"}
    )


@app.post("/contact", response_class=HTMLResponse)
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    return templates.TemplateResponse(
        "contact.html",
        {
            "request": request,
            "nav_links": NAV_LINKS,
            "active": "/contact",
            "submitted": True,
            "name": name,
        },
    )
