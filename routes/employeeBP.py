from flask import Blueprint
from controllers.employeeController import save, find_all, employees_total_productions


employee_blueprint = Blueprint('employee_bp', __name__)

# Save a New Employee
employee_blueprint.route('/', methods=['POST'])(save)

# Get All Employees
employee_blueprint.route('/', methods=['GET'])(find_all)

# Employees Total Productions
employee_blueprint.route('/total-productions', methods=['GET'])(employees_total_productions)