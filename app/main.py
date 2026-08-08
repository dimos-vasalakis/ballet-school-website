import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from app.auth import get_current_user, hash_password, verify_password
from app.database import Base, engine, get_db
from app.models import User

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TParadise Ballet School")
app.add_middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"])

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


def template_globals(request: Request) -> dict:
    db = next(get_db())
    try:
        return {"current_user": get_current_user(request, db)}
    finally:
        db.close()


templates = Jinja2Templates(directory=BASE_DIR / "templates", context_processors=[template_globals])

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


@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse(
        "signup.html", {"request": request, "nav_links": NAV_LINKS, "active": "/signup"}
    )


@app.post("/signup", response_class=HTMLResponse)
async def signup_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):
    error = None
    email = email.strip().lower()

    if password != confirm_password:
        error = "Passwords do not match."
    elif len(password) < 8:
        error = "Password must be at least 8 characters."
    elif db.query(User).filter(User.email == email).first() is not None:
        error = "An account with that email already exists."

    if error:
        return templates.TemplateResponse(
            "signup.html",
            {
                "request": request,
                "nav_links": NAV_LINKS,
                "active": "/signup",
                "error": error,
                "name": name,
                "email": email,
            },
            status_code=400,
        )

    user = User(name=name, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)

    request.session["user_id"] = user.id
    return RedirectResponse(url="/", status_code=303)


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "nav_links": NAV_LINKS, "active": "/login"}
    )


@app.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    email = email.strip().lower()
    user = db.query(User).filter(User.email == email).first()

    if user is None or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "nav_links": NAV_LINKS,
                "active": "/login",
                "error": "Invalid email or password.",
                "email": email,
            },
            status_code=400,
        )

    request.session["user_id"] = user.id
    return RedirectResponse(url="/", status_code=303)


@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
