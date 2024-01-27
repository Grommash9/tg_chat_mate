import pytest
from aiohttp import web

from support_bot.misc import web_routes


@pytest.fixture
def test_client(event_loop, aiohttp_client):
    """
    Test client fixture. Use it to make requests to the server.
    """
    app = web.Application()
    if not app.get("routes_added", False):
        app.add_routes(web_routes)
        app["routes_added"] = True
    return event_loop.run_until_complete(aiohttp_client(app))
