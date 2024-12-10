from flask import Blueprint
from controllers.employeeController import save, find_all, employees_total_productions

employee_blueprint = Blueprint('employee_bp', __name__)
employee_blueprint.route('/', methods=['POST'])(save)
employee_blueprint.route('/', methods=['GET'])(find_all)
employee_blueprint.route('/total-productions', methods=['GET'])(employees_total_productions)