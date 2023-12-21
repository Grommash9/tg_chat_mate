import hashlib
import io
import uuid

from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import set_cors_headers, web_routes
from support_bot.routes.utils import create_option_response, require_auth


@web_routes.post("/tg-bot/file_upload")
@require_auth
async def file_uploading(request: Request):
    data = await request.read()
    file_hash = hashlib.sha256(data).hexdigest()

    existing_file = db.files.find_file_by_hash(file_hash)
    if existing_file:
        response = web.json_response(
            {"error": "file already exists!", "file_id": existing_file["_id"]},
            status=201,
        )
        return set_cors_headers(response)

    file_uuid = str(uuid.uuid4())
    filename = request.headers.get("X-Filename")
    content_type = request.headers.get(
        "Content-Type", "application/octet-stream"
    )
    file_document = {
        "_id": file_uuid,
        "hash": file_hash,
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
    return await create_option_response(request)


@web_routes.get("/tg-bot/file")
@require_auth
async def get_file(request: Request):
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
    response = web.StreamResponse()  # type: ignore[assignment]
    response.headers[
        "CONTENT-DISPOSITION"
    ] = f'attachment; filename="{filename}"'
    response = set_cors_headers(response)
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
async def get_file_options(request: Request):
    return await create_option_response(request)
