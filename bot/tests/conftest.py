import pytest

from support_bot.misc import app, web_routes


@pytest.fixture
def test_client(loop, aiohttp_client):
    """
    Test client fixture. Use it to make requests to the server.
    """
    app.add_routes(web_routes)
    return loop.run_until_complete(aiohttp_client(app))
