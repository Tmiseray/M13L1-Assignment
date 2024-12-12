from flask import request, jsonify
from models.schemas.employeeSchema import employee_schema, employees_schema, employee_production_schema
from services import employeeService
from marshmallow import ValidationError
from caching import cache


# Save New Employee Data
def save():
    try:
        employee_data = employee_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    
    employee_save = employeeService.save(employee_data)
    if employee_save is not None:
        return employee_schema.jsonify(employee_save), 201
    else:
        return jsonify({"message": "Fallback method error activated", "body": employee_data}), 400
    

# Get All Employees
@cache.cached(timeout=60)
def find_all():
    employees = employeeService.find_employees()
    return employees_schema.jsonify(employees), 200


# Employees Total Productions
@cache.cached(timeout=60)
def employees_total_productions():
    try:
        analysis_data = employeeService.employees_total_productions()
        response = employee_production_schema.dump(analysis_data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({ "error": str(e) }), 500