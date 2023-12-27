from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import (
    create_token_for_manager,
    get_manager_username_from_jwt,
    set_cors_headers,
    web_routes,
)
from support_bot.routes.utils import create_option_response, require_auth


@web_routes.post("/tg-bot/login")
async def manager_login(request: Request):
    payload = await request.json()
    user_name = payload.get("user_name")
    password = payload.get("password")
    if not user_name or not password:
        return web.json_response(
            {"error": "Missing username or password"}, status=400
        )

    if not await db.manager.check_password(user_name, password):
        response = web.json_response(
            {"error": "Wrong credentials"}, status=401
        )
        return set_cors_headers(response)
    manager = await db.manager.get_manager_by_username(user_name)

    if manager.get("activated"):
        token = create_token_for_manager(user_name)
        response = web.json_response({"token": token}, status=200)
        return set_cors_headers(response)

    error_text = (
        "Your account is not active yet. Please contact administrator."
    )
    response = web.json_response({"error": error_text}, status=401)
    return set_cors_headers(response)


@web_routes.post("/tg-bot/check_token")
async def manager_check_token(request: Request):
    payload = await request.json()
    token = payload.get("token")
    manager_user_name = get_manager_username_from_jwt(token)
    if manager_user_name is None:
        response = web.json_response(
            {"error": "Wrong token or it was expired"}, status=401
        )
    else:
        response = web.json_response(
            {"token": token, "manager": manager_user_name}, status=200
        )
    return set_cors_headers(response)


@web_routes.get("/tg-bot/get-manager-info")
@require_auth
async def get_manager_info(request: Request):
    manager_info = await db.manager.get_manager_by_username(
        request.get("manager_user_name")
    )
    manager_info["_id"] = str(manager_info["_id"])
    response = web.json_response({"manager_info": manager_info}, status=200)
    return set_cors_headers(response)


@web_routes.post("/tg-bot/registration")
async def manager_registration(request: Request):
    payload = await request.json()
    user_name = payload.get("user_name")
    password = payload.get("password")

    full_name = payload.get("full_name")
    if not user_name or not password or not full_name:
        return web.json_response(
            {"error": "Missing username or password or full name"}, status=400
        )
    if len(password) < 6:
        return web.json_response(
            {"error": "Password should be at least 6 characters long!"},
            status=400,
        )
    await db.manager.new_manager(
        full_name, user_name, password, activated=False
    )
    response = web.json_response({"user_name": user_name}, status=200)
    return set_cors_headers(response)


@web_routes.options("/tg-bot/<action>")
async def manager_option(request: Request):
    return await create_option_response(request)
