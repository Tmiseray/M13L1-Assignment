from flask import Blueprint
from controllers.productionController import save, find_all, production_efficiency


production_blueprint = Blueprint('production_bp', __name__)

# Save a New Production
production_blueprint.route('/', methods=['POST'])(save)

# Get All Productions
production_blueprint.route('/', methods=['GET'])(find_all)

# Production Efficiency Analysis
production_blueprint.route('/efficiency-analysis/<string:date>', methods=['GET'])(production_efficiency)