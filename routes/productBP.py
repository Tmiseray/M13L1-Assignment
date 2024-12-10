from flask import Blueprint
from controllers.productController import save, find_all, top_selling_products


product_blueprint = Blueprint('product_bp', __name__)
product_blueprint.route('/', methods=['POST'])(save)
product_blueprint.route('/', methods=['GET'])(find_all)
product_blueprint.route('/top-selling-products', methods=['GET'])(top_selling_products)