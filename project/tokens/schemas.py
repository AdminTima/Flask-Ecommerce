from marshmallow import Schema, fields


class TokenSchema(Schema):
    refresh = fields.Str(required=True)


