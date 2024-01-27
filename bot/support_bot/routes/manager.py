from aiohttp.web import json_response
from aiohttp.web_request import Request
from pymongo.errors import DuplicateKeyError

from support_bot import db
from support_bot.db.manager import (
    check_password,
    get_manager_by_username,
    hash_password,
    update,
)
from support_bot.misc import (
    create_token_for_manager,
    get_manager_username_from_jwt,
    web_routes,
)
from support_bot.routes.utils import create_option_response, require_auth


@web_routes.post("/tg-bot/manager/login")
async def manager_login(request: Request):
    payload = await request.json()
    try:
        username, password = payload["username"], payload["password"]
    except KeyError:
        return json_response(
            {"error": "Missing username or password"}, status=422
        )

    if not await db.manager.check_password(username, password):
        return json_response({"error": "Wrong credentials"}, status=401)
    manager = await get_manager_by_username(username)

    if manager is not None and manager.activated:
        token = create_token_for_manager(username)
        return json_response({"token": token}, status=200)

    error_text = (
        "Your account is not active yet. Please contact administrator."
    )
    return json_response({"error": error_text}, status=401)


@web_routes.post("/tg-bot/manager/check_token")
async def manager_check_token(request: Request):
    payload = await request.json()
    token = payload.get("token")
    manager_user_name = get_manager_username_from_jwt(token)
    if manager_user_name is None:
        return json_response(
            {"error": "Wrong token or it was expired"}, status=401
        )
    return json_response(
        {"token": token, "manager": manager_user_name}, status=200
    )


@web_routes.post("/tg-bot/manager/change-password")
@require_auth
async def manager_change_password(request: Request):
    payload = await request.json()
    user_name = request["manager_user_name"]
    try:
        new_password = payload["new_password"]
        old_password = payload["old_password"]
    except KeyError:
        return json_response(
            {"result": "new_password or old_password fields missing!"},
            status=422,
        )
    if not await check_password(user_name, old_password):
        return json_response({"result": "Wrong password!"}, status=401)

    hashed_password = hash_password(new_password)
    await update(user_name, {"hashed_password": hashed_password})
    return json_response({"result": "Password changed!"}, status=201)


@web_routes.get("/tg-bot/manager/get-me")
@require_auth
async def get_manager_info(request: Request):
    manager = await get_manager_by_username(request["manager_user_name"])
    if manager is None:
        return json_response({"manager_info": {}}, status=404)
    return json_response({"manager_info": manager.to_dict()}, status=200)


@web_routes.get("/tg-bot/manager")
@require_auth
async def get_managers(request: Request):
    managers = await db.manager.get_managers()
    manager_list = [manager.to_dict() for manager in managers]
    return json_response({"managers": manager_list}, status=200)


@web_routes.patch("/tg-bot/manager")
@require_auth
async def update_manager(request: Request):
    if not request["manager_is_root"]:
        return json_response(
            {"result": "Non-Root manager can`t update manager"}, status=403
        )
    payload = await request.json()
    try:
        username = payload["username"]
    except KeyError:
        return json_response(
            {"result": "Manager username is missing"}, status=422
        )
    update_counter = await update(username, payload)
    if update_counter:
        return json_response({"result": "Manager info updated"}, status=200)
    return json_response(
        {"result": "Manager info was not updated"}, status=500
    )


@web_routes.delete("/tg-bot/manager")
@require_auth
async def delete_manager(request: Request):
    if not request["manager_is_root"]:
        return json_response(
            {"result": "Non-Root manager can`t delete manager"}, status=403
        )
    payload = await request.json()
    try:
        username = payload["username"]
    except KeyError:
        return json_response(
            {"result": "Manager username is missing"}, status=422
        )
    await db.manager.delete_manager_by_username(username)
    return json_response({}, status=204)


@web_routes.post("/tg-bot/manager")
async def manager_registration(request: Request):
    payload = await request.json()
    try:
        username = payload["username"]
        password = payload["password"]
        full_name = payload["full_name"]
    except KeyError:
        return json_response(
            {"error": "Missing username or password or full name"}, status=400
        )
    if len(password) < 6:
        return json_response(
            {"error": "Password should be at least 6 characters long!"},
            status=400,
        )
    try:
        await db.manager.new_manager(
            full_name, username, password, activated=False
        )
    except DuplicateKeyError as e:
        return json_response({"result": str(e)}, status=409)
    return json_response({"result": "ok", "username": username}, status=201)


@web_routes.options("/tg-bot/<action>")
async def manager_option(request: Request):
    return await create_option_response(request)
