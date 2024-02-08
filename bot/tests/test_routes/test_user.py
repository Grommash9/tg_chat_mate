from unittest.mock import AsyncMock

import pytest

from tests.test_utils.fake_objects import FakeDB, FakeRedis
from tests.test_utils.mock_data import (
    FLOOD_CHECK_ERROR,
    INVALID_USER_ID_IN_URL,
    MANAGER_ACTION_WRONG_ACTION,
    NOTIFICATION_FAILED,
    NOTIFICATION_SUCCCESS,
    USER_INFO_UPDATE_SUCCESS,
    USER_NOT_FOUND_ERROR,
    VALID_USER_DOCUMENT,
)


@pytest.mark.parametrize(
    "user_id, status, expected_resp, doc_found",
    [
        ("test_user_id", 400, INVALID_USER_ID_IN_URL, None),
        ("123", 200, VALID_USER_DOCUMENT, VALID_USER_DOCUMENT),
        ("123", 404, {"result": "User not found"}, None),
    ],
)
async def test_get_user_info(
    test_client,
    mocker,
    user_id,
    status,
    expected_resp,
    doc_found,
):
    mocker.patch(
        "support_bot.db.user.get_async_mongo_db",
        side_effect=FakeDB([doc_found]),
    )
    resp = await test_client.get(
        f"/tg-bot/user/{user_id}",
        headers={"AuthorizationToken": "test_token"},
    )
    assert resp.status == status
    data = await resp.json()
    assert data == expected_resp


@pytest.mark.parametrize(
    "user_id, status, expected_resp, modified_count",
    [
        ("test_user_id", 400, INVALID_USER_ID_IN_URL, 0),
        ("123", 200, USER_INFO_UPDATE_SUCCESS, 1),
        ("123", 404, USER_NOT_FOUND_ERROR, 0),
    ],
)
async def test_update_user_info(
    test_client,
    mocker,
    user_id,
    status,
    expected_resp,
    modified_count,
):
    mocker.patch(
        "support_bot.db.user.get_async_mongo_db",
        side_effect=FakeDB([], modified_count=modified_count),
    )
    resp = await test_client.patch(
        f"/tg-bot/user/{user_id}",
        headers={"AuthorizationToken": "test_token"},
        json={"first_name": "John"},
    )

    assert resp.status == status
    data = await resp.json()
    assert data == expected_resp


@pytest.mark.parametrize(
    "action, status, expect_resp, redis_exists, tele_exception",
    [
        ("wrong_action", 400, MANAGER_ACTION_WRONG_ACTION, False, False),
        ("typing", 429, FLOOD_CHECK_ERROR, True, False),
        ("typing", 200, NOTIFICATION_SUCCCESS, False, False),
        ("typing", 500, NOTIFICATION_FAILED, False, True),
    ],
)
async def test_manager_action_notification(
    test_client,
    mocker,
    action,
    status,
    expect_resp,
    redis_exists,
    tele_exception,
):
    mocker.patch(
        "support_bot.routes.utils.aioredis.from_url",
        return_value=FakeRedis(exists=redis_exists),
    )
    side_effect = None
    if tele_exception:
        side_effect = Exception("test")

    mocker.patch(
        "support_bot.routes.user.bot.send_chat_action",
        return_value=AsyncMock(),
        side_effect=side_effect,
    )
    resp = await test_client.post(
        f"/tg-bot/user/123/{action}",
        headers={"AuthorizationToken": "test_token"},
    )

    assert resp.status == status
    data = await resp.json()
    assert data == expect_resp
