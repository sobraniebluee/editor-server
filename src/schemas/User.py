from marshmallow import Schema, fields, validate


class TokensResponse(Schema):
    access_token = fields.String(dump_only=True)


class UserResponse(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(dump_only=True)
    user_type = fields.String(dump_only=True)
    tokens = fields.Nested(TokensResponse(many=False))
    avatar_url = fields.String(dump_only=True)
    message = fields.String(dump_only=True)

