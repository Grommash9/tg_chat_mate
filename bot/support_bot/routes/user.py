from aiohttp import web
from aiohttp.web_request import Request

import support_bot.db.user
from support_bot.misc import bot, web_routes
from support_bot.routes.utils import (
    check_action_flood_protection,
    check_action_value,
    require_auth,
)


@web_routes.get("/tg-bot/user/{user_id}")
@require_auth
async def get_user_info(request: Request):
    try:
        user_id = int(request.match_info["user_id"])
    except (ValueError, TypeError, KeyError) as e:
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
        user_id = int(request.match_info["user_id"])
    except (ValueError, TypeError, KeyError) as e:
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
        user_id = int(request.match_info["user_id"])
        action = check_action_value(request)
    except (ValueError, TypeError, KeyError) as e:
        return web.json_response(
            {"result": f"user_id or action param error: {e}"}, status=400
        )

    flood_protection = await check_action_flood_protection(user_id)
    if flood_protection:
        return web.json_response(
            {"result": "notification don`t pass flood check"}, status=429
        )

    try:
        await bot.send_chat_action(chat_id=user_id, action=action)
    except Exception as e:
        return web.json_response(
            {"result": f"cant send notification to user, error {e}"},
            status=500,
        )

    return web.json_response(
        {"result": "notification sent successfully"}, status=200
    )
