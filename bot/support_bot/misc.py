import datetime
import re
import ssl
from os import getenv

import aiohttp
import jwt
import magic
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from aiohttp import web
from aiohttp.web_request import Request
from bson import Binary

from support_bot import db

ip_address_pattern = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$")

DOMAIN = getenv("DOMAIN", "")
TOKEN = getenv("BOT_TOKEN", "")
WEB_SERVER_HOST = "192.168.1.10"
BASE_WEBHOOK_URL = f"https://{DOMAIN}/tg-bot"
WEBHOOK_SSL_CERT = "/nginx-certs/nginx-selfsigned.crt"
WEBHOOK_SSL_PRIV = "/nginx-certs/nginx-selfsigned.key"
MONGO_USER_NAME = getenv("MONGO_USERNAME")
MONGO_PASSWORD = getenv("MONGO_PASSWORD")
MONGO_HOST = getenv("MONGO_HOST")
MONGO_PORT = getenv("MONGO_PORT")
MONGO_DB_NAME = getenv("MONGO_DB_NAME", "bot_support_db")
LONG_GOOD_SECRET_KEY = getenv(
    "LONG_GOOD_SECRET_KEY", "default_value_if_not_set"
)
ROOT_PASSWORD = getenv("ROOT_PASSWORD")
ISSUE_SSL = getenv("ISSUE_SSL")
WEB_SERVER_PORT = 2005


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def set_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS, GET"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Content-Type, Authorization, AuthorizationToken, X-Filename"
    return response


async def upload_file_to_db_using_file_id(
    file_id: str, base_file_name: str | None = None
):
    file_info = await bot.get_file(file_id)  # type: ignore[union-attr]
    if file_info.file_path is None:
        raise FileNotFoundError
    photo_binary = await bot.download_file(file_info.file_path)
    if photo_binary is None:
        raise FileNotFoundError
    photo_bytes = photo_binary.getvalue()  # type: ignore[attr-defined]
    mime_type = magic.from_buffer(photo_bytes, mime=True)
    file_name = file_info.file_path.split("/")[-1]
    file_data = await upload_file_to_db(
        Binary(photo_binary.getvalue()),  # type: ignore[attr-defined]
        file_name,
        mime_type,
    )  # type: ignore[union-attr]
    return {
        "file_id": file_data["file_id"],
        "mime_type": mime_type,
        "file_name": base_file_name,
    }


def create_token_for_manager(username: str, days=7) -> str | None:
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(
        days=days
    )
    token = jwt.encode(
        {"username": username, "exp": expiration_date},
        LONG_GOOD_SECRET_KEY,
        algorithm="HS256",
    )
    return token


def get_manager_username_from_jwt(token):
    try:
        payload = jwt.decode(
            token,
            LONG_GOOD_SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_signature": True},
        )
        username = payload["username"]
        return username
    except jwt.DecodeError:
        return None  # Invalid token


def get_manager_from_request(request: Request):
    token = (
        request.cookies.get("AUTHToken")
        if request.cookies.get("AUTHToken") is not None
        else request.headers.get("AuthorizationToken")
    )
    if not token:
        return None
    return get_manager_username_from_jwt(token)


async def upload_file_to_db(binary, file_name, mime_type):
    headers = {"X-Filename": file_name, "Content-Type": mime_type}
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        async with session.post(
            f"https://{DOMAIN}/tg-bot/file_upload",
            headers=headers,
            data=binary,
        ) as response:
            print(await response.text())
            return await response.json()


async def send_update_to_socket(message: dict):
    message["_id"] = str(message["date"])
    message["date"] = str(message["date"])
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=ssl_context)
    ) as session:
        async with session.post(
            f"https://{DOMAIN}/send-message",
            json={"message": message},
        ) as resp:
            print(resp.status)
            print(await resp.text())


async def on_startup() -> None:
    try:
        db.manager.new_manager("Root admin", "root", ROOT_PASSWORD, root=True)
    except Exception as e:
        print(f"Can't create root user: {e}")
    if (
        bool(ip_address_pattern.match(DOMAIN))
        and ISSUE_SSL is not None
        and ISSUE_SSL.lower() == "true"
    ):
        result = await bot.set_webhook(
            f"{BASE_WEBHOOK_URL}",
            certificate=FSInputFile(WEBHOOK_SSL_CERT),
            secret_token=LONG_GOOD_SECRET_KEY,
        )
    else:
        result = await tg_bot.set_webhook(
            f"{BASE_WEBHOOK_URL}",
            secret_token=LONG_GOOD_SECRET_KEY,
        )

    print(f"{BASE_WEBHOOK_URL}")
    print(result)


def start_bot() -> None:
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=LONG_GOOD_SECRET_KEY,
    )
    webhook_requests_handler.register(app, path="/tg-bot")

    setup_application(app, dp, bot=bot)
    app.add_routes(web_routes)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


router = Router()
web_routes = web.RouteTableDef()
dp = Dispatcher()
dp.include_router(router)
dp.startup.register(on_startup)
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
app = web.Application(client_max_size=20 * 1024 * 1024)
