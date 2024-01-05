from aiohttp import web
from aiohttp.web_request import Request
from pymongo.errors import DuplicateKeyError

from support_bot import db
from support_bot.misc import (
    create_token_for_manager,
    get_manager_username_from_jwt,
    set_cors_headers,
    web_routes,
)
from support_bot.routes.utils import create_option_response, require_auth


@web_routes.post("/tg-bot/manager/login")
async def manager_login(request: Request):
    payload = await request.json()
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        return web.json_response(
            {"error": "Missing username or password"}, status=400
        )

    if not await db.manager.check_password(username, password):
        response = web.json_response(
            {"error": "Wrong credentials"}, status=401
        )
        return set_cors_headers(response)
    manager = await db.manager.get_manager_by_username(username)

    if manager is not None and manager.activated:
        token = create_token_for_manager(username)
        response = web.json_response({"token": token}, status=200)
        return set_cors_headers(response)

    error_text = (
        "Your account is not active yet. Please contact administrator."
    )
    response = web.json_response({"error": error_text}, status=401)
    return set_cors_headers(response)


@web_routes.post("/tg-bot/manager/check_token")
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


@web_routes.get("/tg-bot/manager/get-me")
@require_auth
async def get_manager_info(request: Request):
    manager = await db.manager.get_manager_by_username(
        request.get("manager_user_name")
    )
    if manager is None:
        response = web.json_response({"manager_info": {}}, status=404)
    else:
        response = web.json_response(
            {"manager_info": manager.to_dict()}, status=200
        )
    return set_cors_headers(response)


@web_routes.get("/tg-bot/manager")
@require_auth
async def get_managers(request: Request):
    managers = await db.manager.get_managers()
    response = web.json_response(
        {"managers": [manager.to_dict() for manager in managers]}, status=200
    )
    return set_cors_headers(response)


@web_routes.patch("/tg-bot/manager")
@require_auth
async def update_manager(request: Request):
    payload = await request.json()
    username = payload.get("username")
    update_counter = await db.manager.update(username, payload)
    if update_counter:
        response = web.json_response(
            {"result": "Manager info updated"}, status=200
        )
    else:
        response = web.json_response(
            {"result": "Manager info was not updated"}, status=500
        )
    return set_cors_headers(response)


@web_routes.delete("/tg-bot/manager")
async def delete_manager(request: Request):
    payload = await request.json()
    username = payload.get("username")
    if not username:
        return web.json_response(
            {"error": "Missing username or password or full name"}, status=400
        )
    await db.manager.delete_manager_by_username(username)
    response = web.json_response({}, status=204)
    return set_cors_headers(response)


@web_routes.post("/tg-bot/manager")
async def manager_registration(request: Request):
    payload = await request.json()
    username = payload.get("username")
    password = payload.get("password")
    full_name = payload.get("full_name")
    if not username or not password or not full_name:
        return web.json_response(
            {"error": "Missing username or password or full name"}, status=400
        )
    if len(password) < 6:
        return web.json_response(
            {"error": "Password should be at least 6 characters long!"},
            status=400,
        )
    try:
        await db.manager.new_manager(
            full_name, username, password, activated=False
        )
    except DuplicateKeyError as e:
        response = web.json_response({"result": str(e)}, status=409)
    else:
        response = web.json_response(
            {"result": "ok", "username": username}, status=200
        )
    return set_cors_headers(response)


@web_routes.options("/tg-bot/<action>")
async def manager_option(request: Request):
    return await create_option_response(request)
