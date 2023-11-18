from aiohttp import web
from aiohttp.web_request import Request
from support_bot import db
from support_bot.misc import web_routes, set_cors_headers
from pymongo import MongoClient, DESCENDING

@web_routes.get("/tg-bot/get-messages/{chat_id}")
async def get_messages_list(request: Request):
    chat_id = int(request.match_info['chat_id'])
    messages_list = db.message.get_all_chat_messages(chat_id)
    response = web.json_response(
        {"messages_list": messages_list}, status=200)
    return set_cors_headers(response)