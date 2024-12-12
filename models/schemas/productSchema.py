from marshmallow import fields, validate
from schema import ma


class ProductSchema(ma.Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    createdBy = fields.Integer(required=True)
    createdAt = fields.Date(dump_only=True)
    updatedBy = fields.Integer(allow_none=True)
    updatedAt = fields.Date(dump_only=True)


class TopProductSchema(ma.Schema):
    productName = fields.String(required=True)
    totalItemsSold = fields.Integer(required=True)


class PaginateProductsSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("products",
                  "totalItems",
                  "totalPages",
                  "currentPage",
                  "perPage")

    products = fields.Nested(ProductSchema, many=True)
    totalItems = fields.Integer(required=True)
    totalPages = fields.Integer(required=True)
    currentPage = fields.Integer(required=True)
    perPage = fields.Integer(required=True)


paginate_products_schema = PaginateProductsSchema()

top_product_schema = TopProductSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
