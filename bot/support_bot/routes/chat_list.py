from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import set_cors_headers, web_routes
from support_bot.routes.utils import require_auth


@web_routes.get("/tg-bot/chat-list")
@require_auth
async def get_chat_list(request: Request):
    chat_list = await db.message.get_chat_list()
    response = web.json_response(
        {"error": "bot get", "chat_list": chat_list}, status=200
    )
    return set_cors_headers(response)
