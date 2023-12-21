from aiogram.types import BufferedInputFile
from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import (
    bot,
    send_update_to_socket,
    set_cors_headers,
    web_routes,
)
from support_bot.routes.utils import require_auth, create_option_response


@web_routes.post("/tg-bot/new-text-message")
@require_auth
async def new_message_from_manager(request: Request):
    payload = await request.json()
    try:
        message = await bot.send_message(
            payload.get("chat_id"), payload.get("text")
        )
        message_document = db.message.new_message(
            message, unread=False, manager_name=request["manager_full_name"]
        )
        await send_update_to_socket(message_document)
        response = web.json_response({"result": "Sent"}, status=200)
    except Exception as e:
        response = web.json_response({"result": str(e)}, status=500)
    return set_cors_headers(response)


@web_routes.post("/tg-bot/new-document-message")
@require_auth
async def new_document_message_from_manager(request: Request):
    payload = await request.json()
    file_attachment = db.files.get_file(payload.get("file_attachment_id"))
    try:
        message = await bot.send_document(
            payload.get("chat_id"),
            caption=payload.get("text"),
            document=BufferedInputFile(
                file_attachment["binary_data"],
                file_attachment["filename"],
            ),
        )
        message_document = db.message.new_message(
            message,
            unread=False,
            attachment={
                "file_id": payload.get("file_attachment_id"),
                "mime_type": file_attachment["content_type"],
                "file_name": file_attachment["filename"],
            },
            manager_name=request["manager_full_name"],
        )
        await send_update_to_socket(message_document)
        response = web.json_response({"result": "Sent"}, status=200)
    except Exception as e:
        response = web.json_response({"result": str(e)}, status=500)
    return set_cors_headers(response)


@web_routes.post("/tg-bot/new-photo-message")
@require_auth
async def new_photo_message_from_manager(request: Request):
    payload = await request.json()
    file_attachment = db.files.get_file(payload.get("file_attachment_id"))
    try:
        message = await bot.send_photo(
            payload.get("chat_id"),
            caption=payload.get("text"),
            photo=BufferedInputFile(
                file_attachment["binary_data"],
                file_attachment["filename"],
            ),
        )
        message_document = db.message.new_message(
            message,
            unread=False,
            attachment={
                "file_id": payload.get("file_attachment_id"),
                "mime_type": file_attachment["content_type"],
                "file_name": file_attachment["filename"],
            },
            manager_name=request["manager_full_name"],
        )
        await send_update_to_socket(message_document)
        response = web.json_response({"result": "Sent"}, status=200)
    except Exception as e:
        response = web.json_response({"result": str(e)}, status=500)
    return set_cors_headers(response)


@web_routes.post("/tg-bot/new-audio-message")
@require_auth
async def new_audio_message_from_manager(request: Request):
    payload = await request.json()
    file_attachment = db.files.get_file(payload.get("file_attachment_id"))
    try:
        message = await bot.send_audio(
            payload.get("chat_id"),
            caption=payload.get("text"),
            audio=BufferedInputFile(
                file_attachment["binary_data"],
                file_attachment["filename"],
            ),
        )
        message_document = db.message.new_message(
            message,
            unread=False,
            attachment={
                "file_id": payload.get("file_attachment_id"),
                "mime_type": file_attachment["content_type"],
                "file_name": file_attachment["filename"],
            },
            manager_name=request["manager_full_name"],
        )
        await send_update_to_socket(message_document)
        response = web.json_response({"result": "Sent"}, status=200)
    except Exception as e:
        response = web.json_response({"result": str(e)}, status=500)
    return set_cors_headers(response)


@web_routes.post("/tg-bot/new-video-message")
@require_auth
async def new_video_message_from_manager(request: Request):
    payload = await request.json()
    file_attachment = db.files.get_file(payload.get("file_attachment_id"))
    try:
        message = await bot.send_video(
            payload.get("chat_id"),
            caption=payload.get("text"),
            video=BufferedInputFile(
                file_attachment["binary_data"],
                file_attachment["filename"],
            ),
        )
        message_document = db.message.new_message(
            message,
            unread=False,
            attachment={
                "file_id": payload.get("file_attachment_id"),
                "mime_type": file_attachment["content_type"],
                "file_name": file_attachment["filename"],
            },
            manager_name=request["manager_full_name"],
        )
        await send_update_to_socket(message_document)
        response = web.json_response({"result": "Sent"}, status=200)
    except Exception as e:
        response = web.json_response({"result": str(e)}, status=500)
    return set_cors_headers(response)


@web_routes.options("/tg-bot/new-video-message")
async def new_video_message_options(request: Request):
    return await create_option_response(request)


@web_routes.options("/tg-bot/new-audio-message")
async def new_audio_message_options(request: Request):
    return await create_option_response(request)


@web_routes.options("/tg-bot/new-photo-message")
async def new_photo_message_options(request: Request):
    return await create_option_response(request)


@web_routes.options("/tg-bot/new-document-message")
async def new_document_message_options(request: Request):
    return await create_option_response(request)


@web_routes.options("/tg-bot/new-text-message")
async def new_text_message_options(request: Request):
    return await create_option_response(request)
