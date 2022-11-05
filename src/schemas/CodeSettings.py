from marshmallow import Schema, validate, fields, pre_dump, post_dump


class CodeSettingsResponse(Schema):
    live_mode = fields.Boolean(dump_only=True)
    read_only = fields.Boolean(dump_only=True)
    password = fields.String(dump_only=True)


class UpdateCodeSettingsRequest(Schema):
    live_mode = fields.Boolean(required=True)
    read_only = fields.Boolean(required=True)
    password = fields.Field(required=True, validate=validate.Length(max=30), allow_none=True)

