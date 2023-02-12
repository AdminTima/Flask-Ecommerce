from .. import base_repository
from ..api_error import ApiError
from ..users.models import Users
from werkzeug.security import check_password_hash
from ..tokens import service as token_service


def login_user(user_data):
    user_in_db = base_repository.find(Users, {"email": user_data["email"]})
    if not user_in_db:
        raise ApiError.not_found("Can't find user with provided credentials")
    is_password_valid = check_password_hash(user_in_db.password, user_data["password"])
    if not is_password_valid:
        raise ApiError(400, "Invalid password")
    payload = {
                "username": user_in_db.username,
                "email": user_in_db.email,
                "id": user_in_db.id,
                "is_staff": user_in_db.is_staff,
                }
    tokens = token_service.generate_tokens(payload)
    token_service.save_token(tokens["refresh"], user_in_db.id)
    return tokens


def logout_user(user_id):
    return token_service.remove_token(user_id)

