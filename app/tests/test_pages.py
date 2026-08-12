import pytest

pytestmark = pytest.mark.asyncio


async def test_home_page(client):
    r = await client.get("/")
    assert r.status_code == 200
    assert "Grace in Every Movement" in r.text


async def test_about_page(client):
    r = await client.get("/about")
    assert r.status_code == 200
    assert "Meet Our Instructors" in r.text
    assert "What Families Say" in r.text


async def test_classes_page(client):
    r = await client.get("/classes")
    assert r.status_code == 200
    assert "Pre-Ballet" in r.text
    assert "Frequently Asked Questions" in r.text


async def test_contact_page(client):
    r = await client.get("/contact")
    assert r.status_code == 200
    assert "Contact Us" in r.text


async def test_robots_txt(client):
    r = await client.get("/robots.txt")
    assert r.status_code == 200
    assert "User-agent" in r.text
