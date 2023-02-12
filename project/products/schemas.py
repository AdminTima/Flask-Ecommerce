from marshmallow import Schema, fields
from ..categories.schemas import CategorySchema
from ..reviews.schemas import ReviewSchema


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    bought_times = fields.Int(dump_only=True)
    photo = fields.Raw(type="file")
    category_id = fields.Int(required=True)
    category = fields.Nested(CategorySchema())
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
    reviews = fields.Nested(ReviewSchema(many=True))
