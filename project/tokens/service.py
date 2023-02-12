import datetime
from .models import Tokens
import jwt
from decouple import config
from ..extensions import db
from ..api_error import ApiError
from .. import base_repository


SECRET_ACCESS_KEY = config("SECRET_ACCESS_KEY")
SECRET_REFRESH_KEY = config("SECRET_REFRESH_KEY")


def generate_tokens(payload):

    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    access_token = jwt.encode(payload, SECRET_ACCESS_KEY, algorithm="HS256")
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=10)
    refresh_token = jwt.encode(payload, SECRET_REFRESH_KEY, algorithm="HS256")

    return {
        "access": access_token,
        "refresh": refresh_token,
    }


def save_token(refresh_token, user_id):
    token_in_db = base_repository.find(Tokens, {"user_id": user_id})
    if token_in_db:
        token_in_db.refresh_token = refresh_token
        db.session.commit()
    else:
        base_repository.create(Tokens, {"refresh_token": refresh_token, "user_id": user_id})


def verify_access_token(access_token):
    return jwt.decode(access_token, SECRET_ACCESS_KEY, algorithms=["HS256"])


def verify_refresh_token(refresh_token):
    payload = jwt.decode(refresh_token, SECRET_REFRESH_KEY, algorithms=["HS256"])
    token_in_db = base_repository.find(Tokens, {"user_id": payload["id"]}, raise_exception=ApiError.unauthorized())
    return payload


def get_new_tokens(refresh_token):
    payload = verify_refresh_token(refresh_token)
    tokens = generate_tokens(payload)
    save_token(tokens["refresh"], payload["id"])
    return tokens


def get_all_tokens():
    return base_repository.get_all(Tokens)


def remove_token(user_id):
    token_in_db = base_repository.find(
        Tokens, {"user_id": user_id},
        raise_exception=ApiError.not_found("No such token in db")
    )
    base_repository.get_by_id_and_remove(Tokens, token_in_db.id)
    return token_in_db


