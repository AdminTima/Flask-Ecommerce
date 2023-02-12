from flask import request, Blueprint, g
from flask_restful import Resource, Api
from . import service
from .schemas import UserSchema, UpdatePasswordSchema
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from ..api_error import ApiError
from ..auth.decorators import auth_required


user_schema = UserSchema()

users_bp = Blueprint("users_bp", __name__, url_prefix="/users")
api = Api(users_bp)


@users_bp.route("/get-user")
@auth_required
def get_user():
    return service.get_user(g.user["id"])


@users_bp.route("/update", methods=["PUT"])
@auth_required
def update_user_data():
    updated_data = UserSchema(only=("username", "email")).load(request.json)
    updated_user = service.update_user_data(g.user["id"], updated_data)
    return UserSchema().dump(updated_user)


@users_bp.route("/change-password", methods=["PUT"])
@auth_required
def change_password():
    password_data = UpdatePasswordSchema().load(request.json)
    service.change_password(g.user["id"], password_data["old_password"], password_data["new_password"])
    return {"msg": "success"}


class UserController(Resource):

    def get(self):
        users = service.get_all_users()
        return UserSchema().dump(users, many=True)

    def post(self):
        user_data = user_schema.load(request.json)
        try:
            new_user = service.register_user(user_data)
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise ApiError(400, "User already exists")
            raise err
        return user_schema.dump(new_user)

    @auth_required
    def delete(self):
        removed_user = service.remove_user(g.user["id"])
        return UserSchema().dump(removed_user)


api.add_resource(UserController, "")
