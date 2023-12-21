from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import (
    get_manager_from_request,
    set_cors_headers,
    web_routes,
)
from support_bot.routes.auth_decorator import require_auth


@web_routes.get("/tg-bot/get-messages/{chat_id}")
@require_auth
async def get_messages_list(request: Request):
    chat_id = int(request.match_info["chat_id"])
    messages_list = db.message.get_all_chat_messages(chat_id)
    response = web.json_response({"messages_list": messages_list}, status=200)
    return set_cors_headers(response)


@web_routes.options("/tg-bot/get-messages/{chat_id}")
async def get_messages_list_option(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)
