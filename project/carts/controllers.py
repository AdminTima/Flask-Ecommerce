from flask import Blueprint, g, request
from flask_restful import Resource, Api
from . import service
from ..auth.decorators import auth_required
from .schemas import CartAmountUpdateSchema
from .schemas import CartItemSchema, CartSchema

carts_bp = Blueprint("carts_bp", __name__, url_prefix="/carts")
api = Api(carts_bp)


@carts_bp.route("")
@auth_required
def get_user_cart():
    user_cart = service.get_user_cart(g.user["id"])
    return CartSchema().dump(user_cart)


@carts_bp.route("/", methods=["POST"])
@auth_required
def add_cart_item():
    cart_item_data = CartItemSchema().load(request.json)
    new_cart_item = service.add_cart_item(g.user["id"], cart_item_data)
    return CartItemSchema().dump(new_cart_item)


@carts_bp.route("/buy")
@auth_required
def buy():
    service.buy(g.user["id"])
    return {"msg": "success"}


class DetailCartItemController(Resource):

    @auth_required
    def put(self, cart_item_id):
        data = CartAmountUpdateSchema().load(request.json)
        cart = service.edit_cart_item_product_amount(cart_item_id,
                                                             g.user,
                                                             data["amount"]
                                                             )
        return CartSchema().dump(cart)

    @auth_required
    def delete(self, cart_item_id):
        cart = service.remove_cart_item(cart_item_id, g.user)
        return CartSchema().dump(cart)


api.add_resource(DetailCartItemController, "/<int:cart_item_id>")
