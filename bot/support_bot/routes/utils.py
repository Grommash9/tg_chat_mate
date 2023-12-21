from functools import wraps

from aiohttp import web
from aiohttp.web_request import Request

from support_bot import db
from support_bot.misc import DOMAIN, get_manager_from_request, set_cors_headers


def require_auth(f):
    @wraps(f)
    async def decorated_function(request: Request, *args, **kwargs):
        if DOMAIN == request.headers.get("Host"):
            request["manager_user_name"] = "root"
            request["manager_full_name"] = "Root admin"
            return await f(request, *args, **kwargs)

        manager_username = get_manager_from_request(request)
        if manager_username is None:
            response = web.json_response(
                {"result": "AuthorizationToken"}, status=401
            )
            return set_cors_headers(response)

        manager = db.manager.get_manager_by_username(manager_username)
        if not manager:
            # Handle case where manager is not found
            response = web.json_response(
                {"result": "ManagerNotFound"}, status=404
            )
            return set_cors_headers(response)

        # Add the manager to the request for downstream usage
        request["manager_user_name"] = manager_username
        request["manager_full_name"] = manager["full_name"]

        return await f(request, *args, **kwargs)

    return decorated_function


async def create_option_response(request: Request):
    response = web.Response(status=200)
    return set_cors_headers(response)
