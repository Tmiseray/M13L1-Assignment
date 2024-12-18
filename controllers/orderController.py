from flask import request, jsonify, Response
from models.schemas.orderSchema import order_schema, orders_schema, paginate_orders_schema
from services import orderService
from marshmallow import ValidationError
from collections import OrderedDict
import json
from caching import cache
from utils.util import token_required, role_required


# Save New Order Data
@token_required
@role_required('admin')
def save():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as ve:
        return jsonify(ve.messages), 400
    
    order_save = orderService.save(order_data)
    if order_save is not None:
        return order_schema.jsonify(order_save), 201
    else:
        return jsonify({"message": "Fallback method error activated", "body": order_data}), 400
    

# Get All Orders
@token_required
@role_required('admin')
@cache.cached(timeout=60)
def find_all():
    orders = orderService.find_orders()
    return orders_schema.jsonify(orders), 200


# Paginate Orders
@token_required
@role_required('admin')
def paginate_orders():
    try:
        page = request.args.get('page', 1, type=int)
        perPage = request.args.get('perPage', 10, type=int)
        
        pagination_data = orderService.paginate_orders(page=page, per_page=perPage)

        totalItems = pagination_data['totalItems']
        totalPages = (totalItems + perPage - 1) // perPage

        response_dict = OrderedDict([
            ('orders', pagination_data['orders']),
            ('totalItems', totalItems),
            ('totalPages', totalPages),
            ('currentPage', page),
            ('perPage', perPage),
        ])

        return Response(
            json.dumps(paginate_orders_schema.dump(response_dict)),
            mimetype='application/json'
        )
    except Exception as e:
        return jsonify({ "error": str(e) }), 500