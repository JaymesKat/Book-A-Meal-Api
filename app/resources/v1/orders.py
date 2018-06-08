import datetime
from flask import jsonify, request, abort
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity
from app.entities.orders import Order

orders_list = [Order(1,1,1), Order(2,2,2), Order(3,3,2), Order(4,4,1)]

order_keys = ['meal_id', 'user_id']

''' This Order class implements GET, PUT, DELETE methods for an Order.'''
class OrderResource(Resource):

    # Get an order by order id 
    # Authorization for caterer and customer
    @jwt_required()
    def get(self, order_id):
        for order_item in orders_list:
            if order_item.id == order_id:
                   response = jsonify({'order': order_item.serialize()})
                   response.status_code = 200
                   return response
        response = jsonify({'message': "No order of given id found"})
        response.status_code = 404
        return response

    # Modify an order
    # Authorization for customer only
    @jwt_required()
    def put(self, order_id):
        if current_identity['is_caterer'] == True:
            response = jsonify({'message':'An admin(caterer) is not allowed to update an order'})
            response.status_code = 403
            return response

        request.get_json(force=True)

        for order_item in orders_list:
            if order_item.id == order_id:
                order_item.meal_id = request.json['meal_id']
                order_item.user_id = current_identity['id']
                order_item.edited = True
                response = jsonify({'order': order_item.serialize()})
                response.status_code = 202
                return response
        
        response = jsonify({'message': 'Order does not exist'})
        response.status_code = 404
        return response

    # Delete an order
    @jwt_required()
    def delete(self, order_id):
        for order_item in orders_list:
            if order_item.id == order_id:
                orders_list.remove(order_item)
                response = jsonify({'Message': 'Order deleted'})
                response.status_code = 202
                return response

        response = jsonify({'Message': 'Order does not exist'})
        response.status_code = 404
        return response
        


class OrderListResource(Resource):

    # Get all orders
    # Authorization for caterer only
    @jwt_required()
    def get(self):        
        if current_identity['is_caterer'] == False:
            response = jsonify({'message':'You must be an admin to access this resource'})
            response.status_code = 403
            return response
        response = jsonify({'orders': [order.serialize() for order in orders_list]})
        response.status_code = 200
        return response

     # Create a new order, handles a selected meal option from the menu, customer role
    @jwt_required()
    def post(self):
        if current_identity['is_caterer'] == True:
            response = jsonify({'message':'An admin(caterer) is not allowed to post an order'})
            response.status_code = 403
            return response

        request.get_json(force=True)
        if not request.json:
            abort(400)

        for key in request.json.keys():
            if key not in order_keys:
                abort(400)


        order_dict = {
            'id': orders_list[-1].id + 1,
            'meal_id': request.json['meal_id'],
            'user_id': current_identity['id']
        }
        order = Order(order_dict['id'], order_dict['meal_id'],order_dict['user_id'])
        orders_list.append(order)
        response = jsonify({'order': order.serialize()})
        response.status_code = 201
        return response

     # Get orders by user_id
   
    # This method returns a list of orders made by a specific user   
    def get_orders(self, user_id):
        user_orders = []
        for order_item in orders_list:
            if order_item.user_id == user_id:
                user_orders.append(user_id)
        return user_orders
