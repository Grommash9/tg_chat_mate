from aiohttp import web
from aiohttp.web_request import Request
from support_bot import db
from support_bot.misc import web_routes, set_cors_headers

@web_routes.post(f"/tg-bot/mark-as-read")
async def new_message_from_manager(request: Request):
    payload = await request.json()
    chat_id = payload.get("chat_id")
    message_id = payload.get("message_id")
    modified_count = db.message.mark_as_read(chat_id, message_id)
    response = web.json_response({"result": "Marked!", "modified_count": modified_count}, status=200)
    return set_cors_headers(response)