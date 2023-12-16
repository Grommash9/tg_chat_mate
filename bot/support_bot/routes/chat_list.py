from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import (
    get_manager_from_request,
    set_cors_headers,
    web_routes,
)


@web_routes.get("/tg-bot/chat-list")
async def get_chat_list(request: Request):
    manager = get_manager_from_request(request)
    if manager is None:
        response = web.json_response(
            {"error": "AuthorizationToken", "chat_list": []}, status=401
        )
        return set_cors_headers(response)
    chat_list = db.message.get_chat_list()
    response = web.json_response(
        {"error": "bot get", "chat_list": chat_list}, status=200
    )
    return set_cors_headers(response)


@web_routes.options("/tg-bot/chat-list")
async def chat_list_option(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)
