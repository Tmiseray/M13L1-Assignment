from flask import request, jsonify
from models.schemas.productSchema import product_schema, products_schema, top_product_schema
from services import productService
from marshmallow import ValidationError
from caching import cache


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
    

@cache.cached(timeout=60)
def find_all():
    products = productService.find_products()
    return products_schema.jsonify(products), 200

def top_selling_products():
    try:
        analysis_data = productService.top_selling_products()
        response = top_product_schema.dump(analysis_data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({ "error": str(e) }), 500