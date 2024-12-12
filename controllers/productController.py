from flask import request, jsonify, Response
from models.schemas.productSchema import product_schema, products_schema, top_product_schema, paginate_products_schema
from services import productService
from marshmallow import ValidationError
from collections import OrderedDict
import json
from caching import cache


# Save New Product Data
def save():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    
    product_save = productService.save(product_data)
    if product_save is not None:
        return product_schema.jsonify(product_save), 201
    else:
        return jsonify({"message": "Fallback method error activated", "body": product_data}), 400
    

# Get All Products
@cache.cached(timeout=60)
def find_all():
    products = productService.find_products()
    return products_schema.jsonify(products), 200


# Paginate Products
def paginate_products():
    try:
        page = request.args.get('page', 1, type=int)
        perPage = request.args.get('perPage', 10, type=int)

        pagination_data = productService.paginate_products(page=page, per_page=perPage)

        totalItems = pagination_data['totalItems']
        totalPages = (totalItems + perPage - 1) // perPage

        response_dict = OrderedDict([
            ('products', pagination_data['products']),
            ('totalItems', totalItems),
            ('totalPages', totalPages),
            ('currentPage', page),
            ('perPage', perPage),
        ])

        return Response(
            json.dumps(paginate_products_schema.dump(response_dict)),
            mimetype='application/json'
            )
    except Exception as e:
        return jsonify({ "error": str(e) }), 500


# Top Selling Products
@cache.cached(timeout=60)
def top_selling_products():
    try:
        analysis_data = productService.top_selling_products()
        response = top_product_schema.dump(analysis_data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({ "error": str(e) }), 500