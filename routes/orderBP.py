from flask import Blueprint
from controllers.orderController import save, find_all, paginate_orders


order_blueprint = Blueprint('order_bp', __name__)

# Save a new Order
order_blueprint.route('/', methods=['POST'])(save)

# Get All Orders
order_blueprint.route('/', methods=['GET'])(find_all)

# Paginate Orders
order_blueprint.route('/paginate', methods=['GET'])(paginate_orders)