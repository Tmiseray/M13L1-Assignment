from flask import request, jsonify
from models.schemas.productionSchema import production_schema, productions_schema, employee_production_schema
from services import productionService
from marshmallow import ValidationError
from caching import cache


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
    

@cache.cached(timeout=60)
def find_all():
    productions = productionService.find_productions()
    return productions_schema.jsonify(productions), 200


def employees_total_productions():
    try:
        analysis_data = productionService.employees_total_productions()
        response = employee_production_schema.dump(analysis_data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({ "error": str(e) }), 500