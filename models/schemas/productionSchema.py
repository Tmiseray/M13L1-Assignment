from marshmallow import fields
from schema import ma

class ProductionSchema(ma.Schema):
    id = fields.Integer(required=False)
    productId = fields.Integer(required=True)
    quantityProduced = fields.Integer(required=True)
    dateProduced = fields.Date(required=True)
    createdAt = fields.DateTime(required=False)
    updatedAt = fields.DateTime(required=False)


production_schema = ProductionSchema()
productions_schema = ProductionSchema(many=True)