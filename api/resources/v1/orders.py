from flask import  jsonify, request, abort, make_response
from flask_restful import Resource

orders = [
         {
            'id': 1,
            'meal_id': 1,
            'date_submitted' : u'2018-04-24',
            'user_id' : 1
        },
        {
            'id': 2,
            'meal_id': 2,
            'date_submitted' : u'2018-04-24',
            'user_id' : 2
        },
        {
            'id': 23,
            'meal_id': 3,
            'date_submitted' : u'2018-04-25',
            'user_id' : 2
        },
        {
            'id': 4,
            'meal_id': 4,
            'date_submitted' : u'2018-04-25',
            'user_id' : 1
        }
    ]

class Order(Resource):

    # Get order by order id - maps to api 
    def get(self, order_id):
        order = [order for order_item in orders if order_item['id'] == order_id]          
        return jsonify({'order': order}, 200)

    # CRUD operations

    # Modify an order
    def put(self, order_id):
        order_to_update = [order for order_item in orders if order_item['id'] == order_id]
        order_to_update = request.json['data']
        order_to_update['date_submitted'] = datetime.date.today().strftime("%Y-%m-%D")
        return jsonify({'Updated Order': order_to_update}, 201)

    # Delete an order
    def delete(self, order_id):
        order = [order for order in orders if order['id'] == order_id]
        if not order:
            abort(404)
        self.orders.remove(order)
        return jsonify({'result': True}, 204)          

class OrderList(Resource):

    # Get all orders
    def get(self):
        return jsonify({'orders': orders}, 200)

     # Create a new order, handles a selected meal option from the menu
    def post(self):
        order = {
            'id': orders[-1]['id'] + 1,
            'meals': request.json['meals'],
            'date_submitted': datetime.date.today().strftime("%Y-%m-%D"),
            'user_id': request.json['user_id']
        }
        orders.append(order)
        return jsonify({'order': order}, 201)

     # Get orders by user_id
    def get_orders(self, user_id):
        user_orders = []
        for order_item in orders:
            if order_item['user_id'] == user_id:
                user_orders.append(user_id)
        return user_orders
