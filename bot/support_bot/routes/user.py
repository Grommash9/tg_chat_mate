from aiohttp import web
from aiohttp.web_request import Request

import support_bot.db.user
from support_bot.misc import web_routes
from support_bot.routes.utils import require_auth


@web_routes.get("/tg-bot/user/{user}")
@require_auth
async def get_user_info(request: Request):
    user_str = request.match_info.get("user")
    if user_str is None:
        return web.json_response({"error": "Incorrect value"}, status=404)
    try:
        user_id = int(user_str)
    except ValueError:
        return web.json_response({"error": "Incorrect value"}, status=404)
    user_info = await support_bot.db.user.get_user(user_id)
    if not user_info:
        return web.json_response({"error": "User not found"}, status=404)
    return web.json_response(user_info, status=200)


@web_routes.put("/tg-bot/user/{user}")
@require_auth
async def user_update(request: Request):
    data = await request.json()
    user_str = request.match_info.get("user")
    if user_str is None:
        return web.json_response({"error": "Incorrect value"}, status=404)
    try:
        user_id = int(user_str)
    except ValueError:
        return web.json_response({"error": "Incorrect value"}, status=404)
    update_user_info = await support_bot.db.user.update(user_id, data)
    if update_user_info:
        return web.json_response({"success": "User info updated"}, status=200)
    return web.json_response({"error": "User not found"}, status=404)
