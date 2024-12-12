from marshmallow import fields, validate
from schema import ma


class OrderSchema(ma.Schema):
    id = fields.Integer(required=False)
    customerId = fields.Integer(required=True)
    productId = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=0))
    totalPrice = fields.Float(required=False)
    createdAt = fields.DateTime(required=False)
    updatedAt = fields.DateTime(required=False)


class PaginateOrdersSchema(ma.Schema):
    class Mets:
        ordered = True
        fields = ("orders",
                  "totalItems",
                  "totalPages",
                  "currentPage",
                  "perPage")
        
    orders = fields.Nested(OrderSchema, many=True)
    totalItems = fields.Integer(required=True)
    totalPages = fields.Integer(required=True)
    currentPage = fields.Integer(required=True)
    perPage = fields.Integer(required=True)


paginate_orders_schema = PaginateOrdersSchema()

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)