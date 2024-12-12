from flask import Blueprint
from controllers.customerController import save, find_all, customers_loyalty_value


customer_blueprint = Blueprint('customer_bp', __name__)

# Save a New Customer
customer_blueprint.route('/', methods=['POST'])(save)

# Get All Customers
customer_blueprint.route('/', methods=['GET'])(find_all)

# Customers Loyalty Value
customer_blueprint.route('/lifetime-loyalty', methods=['GET'])(customers_loyalty_value)