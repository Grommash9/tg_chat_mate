from unittest.mock import AsyncMock

import pytest

from support_bot.data_types import Manager
from tests.test_utils.fake_objects import FakeDB


@pytest.mark.asyncio
async def test_get_user(test_client):
    resp = await test_client.get(
        "/tg-bot/user/sd",
        headers={"AuthorizationToken": "test_token"},
    )
    resp_dict = await resp.json()
    print('-----------------', resp_dict)

    # assert resp_dict["chat_list"] == chat_list_found