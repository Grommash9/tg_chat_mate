import io
import uuid

from aiohttp import web
from aiohttp.web_request import Request
from pymongo import DESCENDING, MongoClient

from support_bot import db
from support_bot.misc import set_cors_headers, web_routes


@web_routes.post(f"/tg-bot/file_upload")
async def file_uploading(request: Request):
    peername = request.transport.get_extra_info('peername')
    if peername is not None:
        host, _ = peername
        if host != '127.0.0.1':
            token = request.headers.get("AuthorizationToken")
            manager = db.manager.get_manager_by_token(token)
            if manager is None:
                response = web.json_response(
                    {"error": "AuthorizationToken", "chat_list": []}, status=401
                )
                return set_cors_headers(response)
    
    data = await request.read()
    file_uuid = str(uuid.uuid4())
    filename = request.headers.get("X-Filename")
    content_type = request.headers.get("Content-Type", "application/octet-stream")
    file_document = {
        "_id": file_uuid,
        "filename": filename,
        "content_type": content_type,
        "binary_data": data,
    }
    db.files.new_file(file_document)
    response = web.json_response(
        {"error": "file uploaded!", "file_id": file_uuid}, status=201
    )
    return set_cors_headers(response)


@web_routes.options("/tg-bot/file_upload")
async def file_upload_options(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)


@web_routes.get("/tg-bot/file")
async def get_file(request: Request):
    peername = request.transport.get_extra_info('peername')
    if peername is not None:
        host, _ = peername
        if host != '127.0.0.1':
            token = request.headers.get("AuthorizationToken")
            manager = db.manager.get_manager_by_token(token)
            if manager is None:
                response = web.json_response(
                    {"error": "AuthorizationToken", "chat_list": []}, status=401
                )
                return set_cors_headers(response)
            
    file_uuid = request.query.get("file_uuid", "")
    file_document = db.files.get_file(file_uuid)
    if not file_document:
        response = web.json_response(
            {"error": "Can't find file!", "file_id": file_uuid}, status=404
        )
        return set_cors_headers(response)
    file_bytes = file_document["binary_data"]
    filename = file_document["filename"]
    content_type = file_document["content_type"]
    file_like_object = io.BytesIO(file_bytes)
    response = web.StreamResponse()
    response.headers["CONTENT-DISPOSITION"] = f'attachment; filename="{filename}"'
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS, GET"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, AuthorizationToken"

    response.content_type = content_type
    await response.prepare(request)
    while True:
        chunk = file_like_object.read(8192)
        if not chunk:
            break
        await response.write(chunk)
    await response.write_eof()
    return set_cors_headers(response)


@web_routes.options("/tg-bot/file")
async def get_file(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)
