from marshmallow import Schema, fields


class OAuthParse(Schema):
    code = fields.String(load_only=True)
    id = fields.String(load_only=True)
