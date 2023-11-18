from aiohttp import web
from aiohttp.web_request import Request
from support_bot import db
from support_bot.misc import web_routes, bot, set_cors_headers, send_update_to_socket


@web_routes.post(f"/tg-bot/new-message")
async def new_message_from_manager(request: Request):
    payload = await request.json()
    chat_id = payload.get("chat_id")
    message = payload.get("text")
    try:
        message = await bot.send_message(chat_id, message)
        db.message.new_message(message)
        await send_update_to_socket(message)
        response = web.json_response({"result": "Sent"}, status=200)
    except Exception as e:
        response = web.json_response({"result": str(e)}, status=500)
    return set_cors_headers(response)



@web_routes.options("/tg-bot/new-message")
async def new_message_options(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)