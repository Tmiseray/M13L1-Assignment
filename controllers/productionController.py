from flask import request, jsonify
from models.schemas.productionSchema import production_schema, productions_schema, production_efficiency_schema
from services import productionService
from marshmallow import ValidationError
from caching import cache


# Save New Production Data
def save():
    try:
        production_data = production_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    
    production_save = productionService.save(production_data)
    if production_save is not None:
        return production_schema.jsonify(production_save), 201
    else:
        return jsonify({"message": "Fallback method error activated", "body": production_data}), 400
    

# Get All Productions
@cache.cached(timeout=60)
def find_all():
    productions = productionService.find_productions()
    return productions_schema.jsonify(productions), 200


# Production Efficiency Analysis
@cache.cached(timeout=60)
def production_efficiency(date):
    try:
        analysis_data = productionService.production_efficiency(date)
        response = production_efficiency_schema.dump(analysis_data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({ "error": str(e) }), 500