from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import bot, send_update_to_socket, set_cors_headers, web_routes


@web_routes.post(f"/tg-bot/new-message")
async def new_message_from_manager(request: Request):
    token = request.headers.get("AuthorizationToken")
    manager = db.manager.get_manager_by_token(token)
    if manager is None:
        response = web.json_response({"result": "AuthorizationToken"}, status=401)
        return set_cors_headers(response)

    payload = await request.json()
    chat_id = payload.get("chat_id")
    message = payload.get("text")
    try:
        message = await bot.send_message(chat_id, message)
        message_document = db.message.new_message(message)
        await send_update_to_socket(message_document)
        response = web.json_response({"result": "Sent"}, status=200)
    except Exception as e:
        response = web.json_response({"result": str(e)}, status=500)
    return set_cors_headers(response)


@web_routes.options("/tg-bot/new-message")
async def new_message_options(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)
