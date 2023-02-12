from flask import request, Blueprint
from . import service
from .schemas import ProductSchema
from ..auth.decorators import staff_only, auth_required
from flask_restful import Resource, Api


products_bp = Blueprint("products_bp", __name__, url_prefix="/products")
api = Api(products_bp)


class ProductController(Resource):

    @auth_required
    def get(self):
        products = service.get_all_products()
        return ProductSchema().dump(products, many=True)

    @auth_required
    def post(self):
        product_data = ProductSchema().load(request.form)
        new_product = service.create_product(product_data, request.files)
        return ProductSchema().dump(new_product)


class DetailProductController(Resource):

    @auth_required
    def get(self, product_id):
        product = service.get_product(product_id)
        return ProductSchema().dump(product)

    @staff_only
    def delete(self, product_id):
        service.delete_product(product_id)
        return {"msg": "success"}

    @staff_only
    def put(self, product_id):
        updated_data = ProductSchema().load(request.form)
        updated_product = service.update_product(product_id, updated_data, request.files)
        return ProductSchema().dump(updated_product)


api.add_resource(ProductController, "")
api.add_resource(DetailProductController, "/<int:product_id>")


