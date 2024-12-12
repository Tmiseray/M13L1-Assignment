from flask import request, jsonify
from models.schemas.customerSchema import customer_schema, customers_schema, loyal_customers_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache


# Save New Customer Data
def save():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    
    customer_save = customerService.save(customer_data)
    if customer_save is not None:
        return customer_schema.jsonify(customer_save), 201
    else:
        return jsonify({"message": "Fallback method error activated", "body": customer_data}), 400
    

# Get All Customers
@cache.cached(timeout=60)
def find_all():
    customers = customerService.find_customers()
    return customers_schema.jsonify(customers), 200


# Customers Loyalty Value
@cache.cached(timeout=60)
def customers_loyalty_value():
    try:
        analysis_data = customerService.customers_loyalty_value()
        response = loyal_customers_schema.dump(analysis_data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({ "error": str(e) }), 500