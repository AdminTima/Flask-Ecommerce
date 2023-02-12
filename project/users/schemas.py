from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UpdatePasswordSchema(Schema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)

