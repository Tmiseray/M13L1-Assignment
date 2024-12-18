from marshmallow import fields
from schema import ma

class UserSchema(ma.Schema):
    id = fields.Integer(required=False)
    username = fields.String(required=True)
    password = fields.String(required=True)
    role = fields.String(required=True)
    accountId = fields.Integer(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)