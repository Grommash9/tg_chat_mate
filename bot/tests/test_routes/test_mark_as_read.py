import pytest

from tests.test_utils.fake_objects import FakeDB


@pytest.mark.parametrize(
    "chat_id, status, expected_resp, modified_count",
    [
        ("123", 200, {"result": "Marked!", "modified_count": 1}, 1),
        ("14523", 200, {"result": "Marked!", "modified_count": 0}, 0),
    ],
)
async def test_mark_chat_as_read(
    test_client,
    mocker,
    chat_id,
    status,
    expected_resp,
    modified_count,
):
    mocker.patch(
        "support_bot.db.message.get_async_mongo_db",
        side_effect=FakeDB([dict()], modified_count),
    )

    resp = await test_client.post(
        "/tg-bot/mark-chat-as-read",
        headers={"AuthorizationToken": "test_token"},
        json={"chat_id": chat_id},
    )
    assert resp.status == status
    data = await resp.json()
    assert data == expected_resp


@pytest.mark.parametrize(
    "chat_id, message_id, status, expected_resp, modified_count",
    [
        ("123", "2342", 200, {"result": "Marked!", "modified_count": 1}, 1),
        ("14523", "15432", 200, {"result": "Marked!", "modified_count": 0}, 0),
    ],
)
async def test_mark_message_as_read(
    test_client,
    mocker,
    chat_id,
    message_id,
    status,
    expected_resp,
    modified_count,
):
    mocker.patch(
        "support_bot.db.message.get_async_mongo_db",
        side_effect=FakeDB([dict()], modified_count),
    )
    resp = await test_client.post(
        "/tg-bot/mark-as-read",
        headers={"AuthorizationToken": "test_token"},
        json={"chat_id": chat_id, "message_id": message_id},
    )
    assert resp.status == status
    data = await resp.json()
    assert data == expected_resp
