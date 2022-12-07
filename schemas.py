from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.Str(required=True, allow_none=False)
    email = fields.Email(required=True, allow_none=False)
    role_id = fields.Int(required=True, allow_none=False)
    password = fields.Str(required=False, allow_none=False, default="")
