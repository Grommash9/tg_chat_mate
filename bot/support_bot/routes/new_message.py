from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import bot, send_update_to_socket, set_cors_headers, web_routes
from aiogram.types import BufferedInputFile


@web_routes.post(f"/tg-bot/new-message")
async def new_message_from_manager(request: Request):
    token = request.cookies.get("AUTHToken")
    if not token:
        token = request.headers.get("AuthorizationToken")
    manager = db.manager.get_manager_by_token(token)
    if manager is None:
        response = web.json_response({"result": "AuthorizationToken"}, status=401)
        return set_cors_headers(response)
    
    payload = await request.json()
    chat_id = payload.get("chat_id")
    message_text = payload.get("text")
    file_attachment_id = payload.get("file_attachment_id")
    try:
        if file_attachment_id is not None:
            file_attachment = db.files.get_file(file_attachment_id)
            if file_attachment["content_type"].startswith("video/"):
                message = await bot.send_video(chat_id, caption=message_text, video=BufferedInputFile(file_attachment["binary_data"], file_attachment["filename"]))
            elif file_attachment["content_type"].startswith("audio/"):
                message = await bot.send_audio(chat_id, caption=message_text, audio=BufferedInputFile(file_attachment["binary_data"], file_attachment["filename"]))
            elif file_attachment["content_type"].startswith("application/") or file_attachment["content_type"].startswith("text/") or file_attachment["content_type"] == "image/svg+xml":
                message = await bot.send_document(chat_id, caption=message_text, document=BufferedInputFile(file_attachment["binary_data"], file_attachment["filename"]))
            elif file_attachment["content_type"].startswith("image/"):
                message = await bot.send_photo(chat_id, caption=message_text, photo=BufferedInputFile(file_attachment["binary_data"], file_attachment["filename"]))
            else:
                raise FileNotFoundError(f"Can't process {file_attachment['content_type']} file type with telegram, please contact administrator")
            message_document = db.message.new_message(message, unread=False, attachment={"file_id": file_attachment_id, "mime_type": file_attachment["content_type"], "file_name": file_attachment["filename"]}, manager_name=manager["full_name"])
        else:
            message = await bot.send_message(chat_id, message_text)
            message_document = db.message.new_message(message, unread=False, manager_name=manager["full_name"])
        await send_update_to_socket(message_document)
        response = web.json_response({"result": "Sent"}, status=200)
    except Exception as e:
        response = web.json_response({"result": str(e)}, status=500)
    return set_cors_headers(response)


@web_routes.options("/tg-bot/new-message")
async def new_message_options(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)
