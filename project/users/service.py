from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users
from ..api_error import ApiError
from ..auth import service as auth_service
from .. import base_repository
from ..carts import service as cart_service


def register_user(user_data):
    user_data["password"] = generate_password_hash(user_data["password"])
    new_user = base_repository.create(Users, user_data)
    cart_service.create_cart(new_user.id)
    return new_user


def get_user(user_id):
    return base_repository.get_by_id(Users, user_id)


def get_all_users():
    return base_repository.get_all(Users)


def remove_user(user_id):
    cart_service.remove_user_cart(user_id)
    auth_service.logout_user(user_id)
    return base_repository.get_by_id_and_remove(Users, user_id)


def update_user_data(user_id, updated_data):
    result = base_repository.get_by_id_and_update(Users, user_id, updated_data)
    auth_service.logout_user(user_id)
    return result


def change_password(user_id, old_password, new_password):
    user_in_db = base_repository.get_by_id(Users, user_id)
    is_valid_password = check_password_hash(user_in_db.password, old_password)
    if not is_valid_password:
        raise ApiError(400, "Invalid password")
    hashed_password = generate_password_hash(new_password)
    auth_service.logout_user(user_id)
    return base_repository.get_by_id_and_update(Users, user_id, {
        "password": hashed_password
    })




