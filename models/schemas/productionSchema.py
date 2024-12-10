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

class EmployeeProductionSchema(ma.Schema):
    employeeName = fields.String(required=True)
    products = fields.Nested('ProductSchema', many=True, required=False)
    totalItemsProduced = fields.Integer(required=True)

employee_production_schema = EmployeeProductionSchema(many=True)

production_schema = ProductionSchema()
productions_schema = ProductionSchema(many=True)