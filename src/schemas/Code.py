from marshmallow import Schema, fields, validate
from src.config import Config
from src.schemas.CodeSettings import CodeSettingsResponse


class CreateCodeRequest(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=64))
    ext = fields.String(required=True, validate=validate.OneOf(Config.AVAILABLE_EXT))
    value = fields.String(required=True)


class UpdateFileRequest(Schema):
    value = fields.String(required=True)


class UpdateCodeRequest(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=64))
    ext = fields.String(required=True, validate=validate.OneOf(Config.AVAILABLE_EXT))


class CodeResponse(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(dump_only=True)
    ext = fields.String(dump_only=True)
    value = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    is_owner = fields.String(dump_only=True)
    settings = fields.Nested(CodeSettingsResponse(many=False))
    message = fields.String(dump_only=True)


def LightCodeResponse(many=False):
    return CodeResponse(only=("id", "title", "ext", "created_at", "updated_at"), many=many)