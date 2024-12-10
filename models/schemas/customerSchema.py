from marshmallow import fields
from schema import ma


class CustomerSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    createdAt = fields.Date(required=False)
    updatedAt = fields.Date(required=False)

    class Meta:
        fields = ("id", "name", "email", "phone", "createdAt", "updatedAt")

class LoyalCustomersSchema(ma.Schema):
    customerName = fields.String(required=True)
    lifetimeLoyaltyValue = fields.Float(required=True)

loyal_customers_schema = LoyalCustomersSchema(many=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)