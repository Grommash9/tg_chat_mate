from aiohttp import web
from aiohttp.web_request import Request

import support_bot.db.user
from support_bot.misc import web_routes
from support_bot.routes.utils import require_auth


@web_routes.get("/tg-bot/user/{user_id}")
@require_auth
async def get_user_info(request: Request):
    try:
        user_id = int(request.match_info.get("user_id"))
    except (ValueError, TypeError) as e:
        return web.json_response({"result": f"user_id param error: {e}"}, status=400)
    user_info = await support_bot.db.user.get_user(user_id)
    if not user_info:
        return web.json_response({"result": "User not found"}, status=404)
    return web.json_response(user_info, status=200)


@web_routes.put("/tg-bot/user/{user_id}")
# @require_auth
async def user_update(request: Request):
    data = await request.json()
    try:
        user_id = int(request.match_info.get("user_id"))
    except (ValueError, TypeError) as e:
        return web.json_response({"result": f"user_id param error: {e}"}, status=400)
    update_user_info = await support_bot.db.user.update(user_id, data)
    if update_user_info:
        return web.json_response({"result": "User info updated"}, status=200)
    return web.json_response({"result": "User not found"}, status=404)
