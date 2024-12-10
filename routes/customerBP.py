from flask import Blueprint
from controllers.customerController import save, find_all, customers_loyalty_value


customer_blueprint = Blueprint('customer_bp', __name__)
customer_blueprint.route('/', methods=['POST'])(save)
customer_blueprint.route('/', methods=['GET'])(find_all)
customer_blueprint.route('/lifetime-loyalty', methods=['GET'])(customers_loyalty_value)