from flask import Blueprint, request, g
from ..users.schemas import UserSchema
from . import service
from .decorators import auth_required

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login_user():
    user_data = UserSchema().load(request.json, partial=("username",))
    return service.login_user(user_data)


@auth_bp.route("/logout")
@auth_required
def logout_user():
    service.logout_user(g.user["id"])
    return {"msg": "logout successfully"}

