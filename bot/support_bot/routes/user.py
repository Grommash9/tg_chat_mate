import aioredis
from aiohttp import web
from aiohttp.web_request import Request

import support_bot.db.user
from support_bot.misc import web_routes, bot
from support_bot.routes.utils import require_auth


async def last_activity(user_id: int, action: str) -> bool:
    redis = aioredis.from_url("redis://192.168.1.111")
    key = f'user:{user_id}'
    if await redis.exists(key):
        await redis.close()
        return True

    await redis.hset(key, 'action', action)
    await redis.expire(key, 5)
    await redis.close()
    return False


@web_routes.get("/tg-bot/user/{user_id}")
@require_auth
async def get_user_info(request: Request):
    try:
        user_id = int(request.match_info.get("user_id", 0))
    except (ValueError, TypeError) as e:
        return web.json_response(
            {"result": f"user_id param error: {e}"}, status=400
        )
    user_info = await support_bot.db.user.get_user(user_id)
    if not user_info:
        return web.json_response({"result": "User not found"}, status=404)
    return web.json_response(user_info, status=200)


@web_routes.patch("/tg-bot/user/{user_id}")
@require_auth
async def user_update(request: Request):
    data = await request.json()
    try:
        user_id = int(request.match_info.get("user_id", 0))
    except (ValueError, TypeError) as e:
        return web.json_response(
            {"result": f"user_id param error: {e}"}, status=400
        )
    update_user_info = await support_bot.db.user.update(user_id, data)
    if update_user_info:
        return web.json_response({"result": "User info updated"}, status=200)
    return web.json_response({"result": "User not found"}, status=404)


@web_routes.post("/tg-bot/user/{user_id}/{action}")
@require_auth
async def manager_action_notification(request: Request):
    try:
        user_id = int(request.match_info.get("user_id", 0))
        action = str(request.match_info.get("action", None))
    except (ValueError, TypeError) as e:
        return web.json_response(
            {"result": f"user_id or action param error: {e}"}, status=400
        )

    user_info = await support_bot.db.user.get_user(user_id)
    if not user_info:
        return web.json_response({"result": "User not found"}, status=404)

    notification = await last_activity(user_id, action)
    if notification:
        return web.json_response('notification don`t pass flood check', status=200)

    await bot.send_chat_action(chat_id=user_id, action=f'{action}')
    return web.json_response('notification sent successfully', status=200)
