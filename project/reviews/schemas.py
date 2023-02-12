from marshmallow import Schema, fields
from ..users.schemas import UserSchema


class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    review_text = fields.Str(required=True)
    product_id = fields.Int()
    user = fields.Nested(UserSchema(), required=True, dump_only=True)
