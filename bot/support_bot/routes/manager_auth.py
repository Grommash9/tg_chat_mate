from aiohttp import web
from aiohttp.web_request import Request
from support_bot import db
from support_bot.misc import bot, send_update_to_socket, set_cors_headers, web_routes


@web_routes.post(f"/tg-bot/login")
async def manager_login(request: Request):
    payload = await request.json()
    user_name = payload.get("user_name")
    password = payload.get("password")
    if not user_name or not password:
        return web.json_response({"error": "Missing username or password"}, status=400)

    if not db.manager.check_password(user_name, password):
        response = web.json_response({"result": "Wrong credentials"}, status=401)
        return response
    token = db.manager.create_token_for_manager(user_name)
    response = web.json_response({"token": token}, status=200)
    return response


@web_routes.options("/tg-bot/login")
async def manager_login_option(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)
