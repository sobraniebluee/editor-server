from marshmallow import Schema, fields, validate


class UserRoomSchema(Schema):
    id_user = fields.String(dump_only=True)
    sid_user = fields.String(dump_only=True)
    is_owner = fields.Boolean(dump_only=True)
