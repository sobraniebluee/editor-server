from marshmallow import Schema, fields, validate


class CompileRequest(Schema):
    id_file = fields.String(dump_only=True)


class OutputCompileResponse(Schema):
    value = fields.String(dump_only=True)
    is_error = fields.Boolean(dump_only=True)
    version_compiler = fields.String(dump_only=True)