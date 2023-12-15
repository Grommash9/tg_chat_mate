from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import set_cors_headers, web_routes


@web_routes.get("/tg-bot/get-messages/{chat_id}")
async def get_messages_list(request: Request):
    token = request.cookies.get("AUTHToken")
    if not token:
        token = request.headers.get("AuthorizationToken")
    manager = db.manager.get_manager_by_token(token)
    if manager is None:
        response = web.json_response({"error": "AuthorizationToken", "messages_list": []}, status=401)
        return set_cors_headers(response)

    chat_id = int(request.match_info["chat_id"])
    messages_list = db.message.get_all_chat_messages(chat_id)
    response = web.json_response({"messages_list": messages_list}, status=200)
    return set_cors_headers(response)


@web_routes.options("/tg-bot/get-messages/{chat_id}")
async def get_messages_list_option(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)
