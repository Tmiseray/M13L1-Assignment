from flask import Blueprint
from controllers.productController import save, find_all, paginate_products, top_selling_products


product_blueprint = Blueprint('product_bp', __name__)

# Save a New Product
product_blueprint.route('/', methods=['POST'])(save)

# Get All Products
product_blueprint.route('/', methods=['GET'])(find_all)

# Paginate Products
product_blueprint.route('/paginate', methods=['GET'])(paginate_products)

# Top Selling Products
product_blueprint.route('/top-selling-products', methods=['GET'])(top_selling_products)