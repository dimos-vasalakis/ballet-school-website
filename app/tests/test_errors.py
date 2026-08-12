import pytest

pytestmark = pytest.mark.asyncio


async def test_unknown_path_returns_styled_404(client):
    r = await client.get("/does-not-exist")
    assert r.status_code == 404
    assert "Page Not Found" in r.text
    assert "site-header" in r.text


async def test_method_not_allowed_returns_405(client):
    r = await client.post("/about")
    assert r.status_code == 405
