from aiohttp import web
from aiohttp.web_request import Request
from support_bot import db
from support_bot.misc import web_routes, set_cors_headers
from pymongo import MongoClient, DESCENDING

@web_routes.get(f"/tg-bot/chat-list")
async def get_chat_list(request: Request):
    chat_list = db.message.get_chat_list()
    response = web.json_response(
        {"error": "bot get", "chat_list": chat_list},
        status=200
    )
    return set_cors_headers(response)
