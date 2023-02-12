from marshmallow import Schema, fields
from ..products.schemas import ProductSchema


class CartItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    product = fields.Nested(ProductSchema())
    amount = fields.Int(default=1)
    total_sum = fields.Int(required=True)


class CartSchema(Schema):
    id = fields.Int(dump_only=True)
    cart_items = fields.Nested(CartItemSchema(many=True))
    total_sum = fields.Int(dump_only=True)


class CartAmountUpdateSchema(Schema):
    amount = fields.Int(required=True)


