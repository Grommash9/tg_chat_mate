from functools import wraps

import aioredis
from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import DOMAIN, get_manager_from_request, set_cors_headers

ACTION_LIST = [
    "typing",
    "upload_photo",
    "record_video",
    "upload_video",
    "record_voice",
    "upload_voice",
    "upload_document",
    "choose_sticker",
    "find_location",
    "record_video_note",
    "upload_video_note",
]


def require_auth(f):
    @wraps(f)
    async def decorated_function(request: Request, *args, **kwargs):
        manager_username = get_manager_from_request(request)
        if manager_username is None:
            if DOMAIN == request.headers.get("Host"):
                return await f(request, *args, **kwargs)
            response = web.json_response(
                {"result": "AuthorizationToken"}, status=401
            )
            return set_cors_headers(response)

        manager = await db.manager.get_manager_by_username(manager_username)
        if not manager:
            # Handle case where manager is not found
            response = web.json_response(
                {"result": "ManagerNotFound"}, status=404
            )
            return set_cors_headers(response)

        # Add the manager to the request for downstream usage
        request["manager_user_name"] = manager_username
        request["manager_full_name"] = manager.full_name

        return await f(request, *args, **kwargs)

    return decorated_function


async def create_option_response(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)


async def check_action_flood_protection(user_id: int) -> bool:
    redis = aioredis.from_url("redis://192.168.1.111")
    key = f"user:{user_id}"
    if await redis.exists(key):
        await redis.close()
        return True

    await redis.set(key, "", 5)
    await redis.close()
    return False


def check_action_value(request: Request) -> str:
    action = request.match_info["action"]
    if action not in ACTION_LIST:
        raise ValueError("Wrong action")
    return action
