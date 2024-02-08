from unittest.mock import AsyncMock

import pytest
from aiohttp import web

from support_bot.data_types import Manager
from support_bot.misc import web_routes


@pytest.fixture(autouse=True)
def mock_authorization(mocker):
    """
    This mock will bypass all authorization checks for all tests.
    """
    manager_obj = Manager(
        hashed_password="hashed_password",
        full_name="full_name",
        root=True,
        activated=True,
        username="username",
    )

    mocker.patch(
        "support_bot.misc.get_manager_username_from_jwt",
        return_value="username",
    )
    mocker.patch(
        "support_bot.db.manager.get_manager_by_username",
        side_effect=AsyncMock(return_value=manager_obj),
    )
    yield


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
