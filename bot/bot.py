import os
import asyncio
import logging
import sys
from os import getenv
from aiohttp import web
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web_request import Request
from aiomysql import Connection, Cursor, DictCursor, connect
from aiogram.types import User
import db
import re

TOKEN = getenv("BOT_TOKEN")
ip_address_pattern = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$")
WEB_SERVER_HOST = "192.168.1.10"
WEB_SERVER_PORT = 2005

WEBHOOK_SECRET = "my-secret"
BASE_WEBHOOK_URL = f"https://{getenv('SERVER_IP_ADDRESS')}/tg-bot"
print("BASE_WEBHOOK_URL", BASE_WEBHOOK_URL)

WEBHOOK_SSL_CERT = "/nginx-certs/nginx-selfsigned.crt"
WEBHOOK_SSL_PRIV = "/nginx-certs/nginx-selfsigned.key"
router = Router()
web_routes = web.RouteTableDef()

@web_routes.get(f"/tg-bot/get_users")
async def get_200(request: Request):
    users_data = db.user.get_all_users()
    return web.json_response(
        {"error": "bot get", "users": users_data}, status=200)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db.user.new_user(message.from_user)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
        db.message.new_message(message)
    except TypeError:
        await message.answer("Nice try!")


async def on_startup(bot: Bot) -> None:
    if bool(ip_address_pattern.match(getenv('SERVER_IP_ADDRESS'))):
        result = await bot.set_webhook(
            f"{BASE_WEBHOOK_URL}",
            certificate=FSInputFile(WEBHOOK_SSL_CERT),
            secret_token=WEBHOOK_SECRET,
        )
    else:
        result = await bot.set_webhook(
            f"{BASE_WEBHOOK_URL}",
            certificate=FSInputFile(WEBHOOK_SSL_CERT),
            secret_token=WEBHOOK_SECRET,
        )
        
    print(f"{BASE_WEBHOOK_URL}")
    print(result)

def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)



    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path="/tg-bot")

    setup_application(app, dp, bot=bot)
    app.add_routes(web_routes)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
