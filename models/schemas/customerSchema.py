from marshmallow import fields
from schema import ma


class CustomerSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    createdAt = fields.DateTime(required=False)
    updatedAt = fields.DateTime(required=False)

    class Meta:
        fields = ("id", "name", "email", "phone", "createdAt", "updatedAt")


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)