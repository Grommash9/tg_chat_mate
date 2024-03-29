from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import set_cors_headers, web_routes
from support_bot.routes.utils import create_option_response, require_auth


@web_routes.get("/tg-bot/get-messages/{chat_id}")
@require_auth
async def get_messages_list(request: Request):
    chat_id = int(request.match_info["chat_id"])
    messages_list = await db.message.get_all_chat_messages(chat_id)
    response = web.json_response({"messages_list": messages_list}, status=200)
    return set_cors_headers(response)


@web_routes.options("/tg-bot/get-messages/{chat_id}")
async def get_messages_list_option(request: Request):
    return await create_option_response(request)
