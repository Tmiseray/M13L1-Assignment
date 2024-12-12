from marshmallow import fields
from schema import ma

class ProductionSchema(ma.Schema):
    id = fields.Integer(required=False)
    productId = fields.Integer(required=True)
    quantityProduced = fields.Integer(required=True)
    dateProduced = fields.Date(required=True)
    createdBy = fields.Integer(required=True)
    createdAt = fields.Date(dump_only=True)
    updatedBy = fields.Integer(allow_none=True)
    updatedAt = fields.Date(dump_only=True)


class ProductionEfficiencySchema(ma.Schema):
    productName = fields.String(required=True)
    productionDate = fields.Date(required=True)
    quantityProducedOnDate = fields.Integer(required=True)


production_efficiency_schema = ProductionEfficiencySchema(many=True)

production_schema = ProductionSchema()
productions_schema = ProductionSchema(many=True)