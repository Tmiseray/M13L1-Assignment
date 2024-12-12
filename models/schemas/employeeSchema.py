from marshmallow import fields
from schema import ma


class EmployeeSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    position = fields.String(required=True)
    createdAt = fields.Date(required=False)
    updatedAt = fields.Date(required=False)

    class Meta:
        fields = ("id", "name", "position", "createdAt", "updatedAt")


class EmployeeProductionSchema(ma.Schema):
    employeeName = fields.String(required=True)
    products = fields.Nested('ProductSchema', many=True, required=False)
    totalItemsProduced = fields.Integer(required=True)


employee_production_schema = EmployeeProductionSchema(many=True)

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)