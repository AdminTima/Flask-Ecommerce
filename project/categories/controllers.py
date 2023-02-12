from flask_restful import Resource, Api
from flask import request, Blueprint
from .schemas import CategorySchema
from . import service
from ..auth.decorators import staff_only, auth_required
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from ..api_error import ApiError


categories_bp = Blueprint("categories_bp", __name__, url_prefix="/categories")
api = Api(categories_bp)


class CategoryController(Resource):

    @auth_required
    def get(self):
        categories = service.get_all_categories()
        return CategorySchema().dump(categories, many=True)

    @staff_only
    def post(self):
        category_data = CategorySchema().load(request.json)
        try:
            new_category = service.create_category(category_data)
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise ApiError.bad_request("Category with this name already exists")
            raise err
        return CategorySchema().dump(new_category)


class DetailCategoryController(Resource):

    def delete(self, category_id):
        deleted_category = service.delete_category(category_id)
        return CategorySchema().dump(deleted_category)

    def put(self, category_id):
        category_data = CategorySchema().dump(request.json)
        updated_category = service.update_category(category_id, category_data)
        return CategorySchema().dump(updated_category)


api.add_resource(CategoryController, "")
api.add_resource(DetailCategoryController, "/<int:category_id>")
