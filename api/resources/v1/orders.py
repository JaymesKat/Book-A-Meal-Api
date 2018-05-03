import datetime
from flask import  jsonify, request, abort
from flask_restful import Resource
from flask_jwt import JWT, jwt_required

orders = [
         {
            'id': 1,
            'meal_id': 1,
            'date_submitted' : '2018-04-24',
            'user_id' : 1
        },
        {
            'id': 2,
            'meal_id': 2,
            'date_submitted' : '2018-04-24',
            'user_id' : 2
        },
        {
            'id': 3,
            'meal_id': 3,
            'date_submitted' : '2018-04-25',
            'user_id' : 2
        },
        {
            'id': 4,
            'meal_id': 4,
            'date_submitted' : '2018-04-25',
            'user_id' : 1
        }
    ]

    
order_keys = ['meal_id', 'user_id']

class Order(Resource):

    # Get order by order id - maps to api 
    def get(self, order_id):
        order = [order_item for order_item in orders if order_item['id'] == order_id]          
        if not order:
            abort(404)
        return jsonify({'order': order}, 200)

    # CRUD operations

    # Modify an order
    def put(self, order_id):
        request.get_json(force=True)

        order_to_update = [order_item for order_item in orders if order_item['id'] == order_id]
        order_to_update[0]['meal_id'] = request.json['meal_id']
        order_to_update[0]['user_id'] = request.json['user_id']
        order_to_update[0]['date_submitted'] = datetime.date.today().strftime("%Y-%m-%D")
        
        response = jsonify({'order': order_to_update})
        response.status_code = 200
        return response

    # Delete an order
    def delete(self, order_id):
        order_to_delete = [order_item for order_item in orders if order_item['id'] == order_id]
        if not order_to_delete[0]:
            abort(404)
        orders.remove(order_to_delete[0])
        response = jsonify({'result': True})
        response.status_code = 204
        return response

class OrderList(Resource):

    # Get all orders
    def get(self):
        response = jsonify({'orders': orders})
        response.status_code = 200
        return response

     # Create a new order, handles a selected meal option from the menu
    def post(self):
        request.get_json(force=True)
        if not request.json:
            abort(400)

        for key in request.json.keys():
            if key not in order_keys:
                abort(400)

        order = {
            'id': orders[-1]['id'] + 1,
            'meal_id': request.json['meal_id'],
            'date_submitted': datetime.date.today().strftime("%Y-%m-%d"),
            'user_id': request.json['user_id']
        }
        orders.append(order)
        response = jsonify({'order': order})
        response.status_code = 201
        return response

     # Get orders by user_id
    
    def get_orders(self, user_id):
        user_orders = []
        for order_item in orders:
            if order_item['user_id'] == user_id:
                user_orders.append(user_id)
        return user_orders
