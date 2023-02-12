import functools
from flask import request, g
from project.api_error import ApiError
from project.tokens.service import verify_access_token


def get_token_from_header(req):
    auth_header = req.headers.get("authorization", None)
    if not auth_header:
        raise ApiError.unauthorized()
    try:
        if auth_header[:6] != "Bearer":
            raise ApiError.unauthorized()
        access_token = auth_header.split(" ")[1]
    except KeyError:
        raise ApiError.unauthorized()
    return access_token


def auth_required(view):
    @functools.wraps(view)
    def inner(*args, **kwargs):
        access_token = get_token_from_header(request)
        payload = verify_access_token(access_token)
        g.user = payload
        return view(*args, **kwargs)
    return inner


def staff_only(view):
    @functools.wraps(view)
    def inner(*args, **kwargs):
        access_token = get_token_from_header(request)
        payload = verify_access_token(access_token)
        if not payload.get("is_staff", None):
            raise ApiError(403, "You have no permissions to perform this action")
        return view(*args, **kwargs)
    return inner





