from unittest.mock import AsyncMock

import pytest

from support_bot.data_types import Manager
from tests.test_utils.fake_objects import FakeDB


@pytest.fixture(autouse=True)
def mock_authorization(mocker):
    """
    This mock will bypass all authorization checks for all tests in this file.
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


@pytest.mark.asyncio
async def test_get_chat_list(mocker, test_client):
    chat_list_found = [
        {
            "user_id": "test_id",
            "last_message_text": "test_text",
            "unread_count": 0,
            "last_message_time": "2021-01-01T00:00:00.000Z",
            "photo_uuid": "test_uuid",
            "username": "test_username",
            "name": "test_name",
        }
    ]
    get_db_mock = mocker.patch(
        "support_bot.db.message.get_async_mongo_db",
        side_effect=FakeDB(chat_list_found),
    )

    resp = await test_client.get(
        "/tg-bot/chat-list",
        headers={"AuthorizationToken": "test_token"},
    )
    resp_dict = await resp.json()

    assert get_db_mock.call_count == 1
    assert resp_dict["chat_list"] == chat_list_found
