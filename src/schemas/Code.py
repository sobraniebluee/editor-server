from marshmallow import Schema, fields, validate, pre_dump
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
    is_owner = fields.Boolean(dump_only=True)
    settings = fields.Nested(CodeSettingsResponse(many=False))
    message = fields.String(dump_only=True)
    is_executable = fields.Boolean(dump_only=True)

    @pre_dump
    def check(self, data, **kwargs):
        # if not data.is_owner:
        #     if data.settings.password is not None:
        #         data.settings.is_password = True
        #         data.settings.password = None
        #     else:
        #         data.settings.is_password = False
        return data


def LightCodeResponse(many=False):
    return CodeResponse(only=("id", "title", "ext", "created_at", "updated_at", "is_executable"), many=many)