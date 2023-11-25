import re
from os import getenv

import aiohttp
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from support_bot import db

ip_address_pattern = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$")


# TODO change after local dev
# LOCAL DEV
# DOMAIN = "ddd0-86-30-162-24.ngrok-free.app"
# TOKEN = "6703786868:AAGep_3TuaTsirZFBm0hrLRSHYs6OL9g1ZA"
# WEB_SERVER_HOST = "127.0.0.1"
# BASE_WEBHOOK_URL = "https://ddd0-86-30-162-24.ngrok-free.app/tg-bot"
# MONGO_USER_NAME = "root"
# MONGO_PASSWORD = "root"
# MONGO_HOST = "127.0.0.1"
# MONGO_PORT = 27016
# MONGO_DB_NAME = "support_db_table"
# LONG_GOOD_SECRET_KEY = "somekey"
# ROOT_PASSWORD = "somepass"

# PROD
DOMAIN = getenv("DOMAIN")
TOKEN = getenv("BOT_TOKEN")
WEB_SERVER_HOST = "192.168.1.10"
BASE_WEBHOOK_URL = f"https://{DOMAIN}/tg-bot"
WEBHOOK_SSL_CERT = "/nginx-certs/nginx-selfsigned.crt"
WEBHOOK_SSL_PRIV = "/nginx-certs/nginx-selfsigned.key"
MONGO_USER_NAME = getenv("MONGO_USERNAME")
MONGO_PASSWORD = getenv("MONGO_PASSWORD")
MONGO_HOST = getenv("DOMAIN")
MONGO_PORT = getenv("MONGO_PORT")
MONGO_DB_NAME = getenv("MONGO_DB_NAME")
LONG_GOOD_SECRET_KEY = getenv("LONG_GOOD_SECRET_KEY")
ROOT_PASSWORD = getenv("ROOT_PASSWORD")

WEB_SERVER_PORT = 2005


def set_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS, GET"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, AuthorizationToken"
    return response

async def send_update_to_socket(message: Message):
    async with aiohttp.ClientSession() as session:
        post_data = {
            "text": message.text,
            "chat_id": message.chat.id,
            "from_user_id": message.from_user.id,
        }
        async with session.post(
            f"https://{DOMAIN}/send-message", json=post_data,
        ) as resp:
            print(resp.status)
            print(await resp.text())


async def on_startup(bot: Bot) -> None:
    try:
        db.manager.new_manager("Root admin", "root", ROOT_PASSWORD, root=True)
    except Exception as e:
        print(f"Can't create root user: {e}")
    if DOMAIN is not None and bool(
        ip_address_pattern.match(DOMAIN)
    ):
        result = await bot.set_webhook(
            f"{BASE_WEBHOOK_URL}",
            certificate=FSInputFile(WEBHOOK_SSL_CERT),
            secret_token=LONG_GOOD_SECRET_KEY,
        )
    else:
        result = await bot.set_webhook(
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
app = web.Application()
