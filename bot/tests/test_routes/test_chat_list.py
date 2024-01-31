import pytest

from tests.test_utils.fake_objects import FakeDB


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
