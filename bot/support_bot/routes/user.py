from aiohttp import web
from aiohttp.web_request import Request

import support_bot.db.user
from support_bot.misc import web_routes
from support_bot.routes.utils import require_auth


@web_routes.patch("/tg-bot/user")
@require_auth
async def user(request: Request):
    data = await request.json()
    user_id = int(data.get("user_id"))
    del data["user_id"]
    await support_bot.db.user.update(user_id, data)
    return web.json_response({"success": ""}, status=200)
