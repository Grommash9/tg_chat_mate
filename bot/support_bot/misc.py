from os import getenv
from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, Message
import aiohttp
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import re

ip_address_pattern = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$")


#TODO change after local dev
# LOCAL DEV
# TOKEN = "663133610N2UifJRGXkw"
# WEB_SERVER_HOST = "127.0.0.1"
# BASE_WEBHOOK_URL = "https://ok-free.app/tg-bot"
# MONGO_USER_NAME = "root"
# MONGO_PASSWORD = "root"
# MONGO_HOST = "127.0.0.1"
# MONGO_PORT = 27016
# MONGO_DB_NAME = "support_db_table"

# PROD
SERVER_IP_ADDRESS = getenv('SERVER_IP_ADDRESS')
TOKEN = getenv("BOT_TOKEN")
WEB_SERVER_HOST = "192.168.1.10"
BASE_WEBHOOK_URL = f"https://{SERVER_IP_ADDRESS}/tg-bot"
WEBHOOK_SSL_CERT = "/nginx-certs/nginx-selfsigned.crt"
WEBHOOK_SSL_PRIV = "/nginx-certs/nginx-selfsigned.key"
MONGO_USER_NAME = getenv("MONGO_USERNAME")
MONGO_PASSWORD = getenv("MONGO_PASSWORD")
MONGO_HOST = getenv('SERVER_IP_ADDRESS')
MONGO_PORT = getenv("MONGO_PORT")
MONGO_DB_NAME = getenv("MONGO_DB_NAME")

WEB_SERVER_PORT = 2005
WEBHOOK_SECRET = "my-secret"

def set_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

async def send_update_to_socket(message: Message):
    async with aiohttp.ClientSession() as session:
        post_data = {'text': message.text, 'chat_id': message.chat.id, "from_user_id": message.from_user.id}
        #TODO ADD SSL VERIFICATION IGNORING FOR SELF SIGNED SERTIFICATE BOT WORKING WELL
        async with session.post(f'https://{SERVER_IP_ADDRESS}/send-message', json=post_data) as resp:
            print(resp.status)
            print(await resp.text())



async def on_startup(bot: Bot) -> None:
    if getenv('SERVER_IP_ADDRESS') is not None and bool(ip_address_pattern.match(getenv('SERVER_IP_ADDRESS'))):
        result = await bot.set_webhook(
            f"{BASE_WEBHOOK_URL}",
            certificate=FSInputFile(WEBHOOK_SSL_CERT),
            secret_token=WEBHOOK_SECRET,
        )
    else:
        result = await bot.set_webhook(
            f"{BASE_WEBHOOK_URL}",
            secret_token=WEBHOOK_SECRET,
        )
        
    print(f"{BASE_WEBHOOK_URL}")
    print(result)

def start_bot() -> None:
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
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

