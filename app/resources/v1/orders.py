import datetime
from flask import jsonify, request, abort
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity
from app.models import Order
from app import ma

order_keys = ['meal_id', 'user_id']

class OrderSchema(ma.Schema):
    class Meta:
        model = Order


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

''' This Order class implements GET, PUT, DELETE methods for an Order.'''
class OrderResource(Resource):

    # Get an order by order id 
    # Authorization for caterer and customer
    @jwt_required()
    def get(self, order_id):
        order = Order.query.get(order_id)
        if order:
            response = jsonify({"Order": order_schema.dump(order)})
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

        order = Order.query.get(order_id)
        if order:
            order.user_id= current_identity['id']
            order.edited = True
            order.save()
            response = jsonify({'order': order_schema.dump(order)})
            response.status_code = 202
            return response
        
        response = jsonify({'message': 'Order does not exist'})
        response.status_code = 404
        return response

    # Delete an order
    @jwt_required()
    def delete(self, order_id):
        order = Order.query.get(order_id)
        if order:
            order.delete()
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
        orders = Order.query.all()    
        response = jsonify({'orders': orders_schema.dump(orders)})
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
            'meal_id': request.json['meal_id'],
            'user_id': current_identity['id']
        }
        order = Order(order_dict['meal_id'],order_dict['user_id'])
        order.save()
        response = jsonify({'order': order.serialize()})
        response.status_code = 201
        return response
