from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import hash_password, verify_password
from app.csrf import verify_csrf
from app.database import get_db
from app.models import User
from app.rate_limit import limiter
from app.templating import render

router = APIRouter()


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return RedirectResponse(url="/login?view=signup", status_code=307)


@router.post("/signup", response_class=HTMLResponse, dependencies=[Depends(verify_csrf)])
@limiter.limit("5/minute")
async def signup_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    error = None
    email = email.strip().lower()

    if password != confirm_password:
        error = "Passwords do not match."
    elif len(password) < 8:
        error = "Password must be at least 8 characters."
    elif len(password.encode("utf-8")) > 72:
        error = "Password must be at most 72 characters."
    elif (
        await db.execute(select(User).where(User.email == email))
    ).scalar_one_or_none() is not None:
        error = "An account with that email already exists."

    if error:
        return await render(
            request,
            db,
            "login.html",
            "/login",
            view="signup",
            error=error,
            name=name,
            email=email,
            status_code=400,
        )

    user = User(name=name, email=email, hashed_password=await hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)

    request.session["user_id"] = user.id
    return RedirectResponse(url="/", status_code=303)


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, view: str = "login", db: AsyncSession = Depends(get_db)):
    return await render(request, db, "login.html", "/login", view=view)


@router.post("/login", response_class=HTMLResponse, dependencies=[Depends(verify_csrf)])
@limiter.limit("5/minute")
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    email = email.strip().lower()
    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()

    if user is None or not await verify_password(password, user.hashed_password):
        return await render(
            request,
            db,
            "login.html",
            "/login",
            view="login",
            error="Invalid email or password.",
            email=email,
            status_code=400,
        )

    request.session["user_id"] = user.id
    return RedirectResponse(url="/", status_code=303)


@router.post("/logout", dependencies=[Depends(verify_csrf)])
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
