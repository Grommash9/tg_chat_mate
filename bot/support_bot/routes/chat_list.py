from aiohttp import web
from aiohttp.web_request import Request
from support_bot import db
from support_bot.misc import web_routes
from pymongo import MongoClient, DESCENDING

@web_routes.get(f"/tg-bot/chat-list")
async def get_chat_list(request: Request):
    chat_list = db.message.get_chat_list()
    response = web.json_response(
        {"error": "bot get", "chat_list": chat_list},
        status=200
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
