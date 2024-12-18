from services import userService
from flask import jsonify, request
from models.schemas.userSchema import user_schema, users_schema
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, role_required

# User Login
def login():
    userRequest = request.json
    user = userService.login(userRequest['username'], userRequest['password'])
    if user:
        return jsonify(user), 200
    else:
        resp = {
            "status": "error",
            "message": "User does not exist"
        }
        return jsonify(resp), 404
    

# Save New User Data
# @token_required
# @role_required('admin')
def save():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    
    user_save = userService.save(user_data)
    if user_save is not None:
        return user_schema.jsonify(user_save), 201
    else:
        return jsonify({ "message": "Fallback method error activated", "body": user_data }), 400
    

# Get All Users
@token_required
@role_required('admin')
@cache.cached(timeout=60)
def find_all():
    users = userService.find_users()
    return users_schema.jsonify(users), 200

