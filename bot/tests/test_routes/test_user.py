import pytest


@pytest.mark.asyncio
async def test_get_user(test_client):
    resp = await test_client.get(
        "/tg-bot/user/sd",
        headers={"AuthorizationToken": "test_token"},
    )
    resp_dict = await resp.json()
    print("-----------------", resp_dict)
