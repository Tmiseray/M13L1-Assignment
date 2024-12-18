from flask import Blueprint
from controllers.userController import login

user_blueprint = Blueprint('userBP', __name__)
user_blueprint.route('/login', methods=['POST'])(login)