import pytest
from sqlalchemy import select

from app.models import User

pytestmark = pytest.mark.asyncio


async def signup(client, email="jane@example.com", password="supersecret"):
    return await client.post(
        "/signup",
        data={
            "name": "Jane Doe",
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )


async def test_signup_success(client, db_session):
    r = await signup(client)
    assert r.status_code == 303
    assert r.headers["location"] == "/"

    async with db_session() as db:
        user = (
            await db.execute(select(User).where(User.email == "jane@example.com"))
        ).scalar_one_or_none()
    assert user is not None
    assert user.name == "Jane Doe"


async def test_signup_duplicate_email(client, db_session):
    await signup(client)
    r = await signup(client)
    assert r.status_code == 400
    assert "already exists" in r.text

    async with db_session() as db:
        count = len((await db.execute(select(User).where(User.email == "jane@example.com"))).all())
    assert count == 1


async def test_signup_password_mismatch(client):
    r = await client.post(
        "/signup",
        data={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "supersecret",
            "confirm_password": "different",
        },
    )
    assert r.status_code == 400
    assert "do not match" in r.text


async def test_signup_short_password(client):
    r = await client.post(
        "/signup",
        data={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "short",
            "confirm_password": "short",
        },
    )
    assert r.status_code == 400
    assert "at least 8 characters" in r.text


async def test_login_success(client):
    await signup(client)
    r = await client.post("/login", data={"email": "jane@example.com", "password": "supersecret"})
    assert r.status_code == 303
    assert r.headers["location"] == "/"


async def test_login_wrong_password(client):
    await signup(client)
    r = await client.post("/login", data={"email": "jane@example.com", "password": "wrongpass"})
    assert r.status_code == 400
    assert "Invalid email or password" in r.text


async def test_login_nonexistent_user(client):
    r = await client.post("/login", data={"email": "nobody@example.com", "password": "whatever"})
    assert r.status_code == 400
    assert "Invalid email or password" in r.text


async def test_logout_clears_session(client):
    await signup(client)
    home = await client.get("/")
    assert "Hi, Jane Doe" in home.text

    r = await client.post("/logout")
    assert r.status_code == 303

    home_after = await client.get("/")
    assert "Hi, Jane Doe" not in home_after.text
    assert "Log In" in home_after.text


async def test_contact_submit_shows_thank_you(client):
    r = await client.post(
        "/contact",
        data={"name": "Jane Doe", "email": "jane@example.com", "message": "Hello!"},
    )
    assert r.status_code == 200
    assert "Thank you, Jane Doe" in r.text
