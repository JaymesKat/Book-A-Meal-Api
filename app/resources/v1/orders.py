from flask import jsonify, request, abort
from flask_restful import Resource
from flask_jwt import current_identity, jwt_required
from app.models import Order, User, Meal
from app import ma


class OrderSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "meal_id", "date_submitted")


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
        if current_identity.is_caterer:
            abort(
                403,
                description='An admin(caterer) is not allowed\
                to update an order')

        request.get_json(force=True)
        meal_id = request.json['meal_id']
        if not isinstance(meal_id, int):
            abort(400, description="Invalid meal id has been entered")

        order = Order.query.get(order_id)
        if order:
            order.user_id = current_identity.id
            meal = Meal.query.get(meal_id)

            if not meal:
                abort(400, description="Meal does not exist")

            order.meal_id = meal.id
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
        if not current_identity.is_caterer:
            abort(
                403,
                description='You must be an admin\
                to access this resource')

        orders = Order.query.all()
        response = jsonify({'orders': orders_schema.dump(orders)})
        response.status_code = 200
        return response

    @jwt_required()
    def post(self):
        '''
            Create a new order, handles a selected meal option
            from the menu, customer role
        '''
        if current_identity.is_caterer:
            abort(
                403,
                description='An admin(caterer) is not allowed to post an order')

        request.get_json(force=True)
        if not request.json:
            abort(400)

        if 'meal_id' not in request.json.keys():
            abort(400)

        meal_id = request.json['meal_id']
        if not isinstance(meal_id, int):
            abort(400, description="Invalid meal id has been entered")

        user = User.query.get(current_identity.id)
        meal = Meal.query.get(meal_id)

        if meal:
            order = Order(meal_id=meal.id, user_id=user.id)
            order.save()

            order = order_schema.dump(order)
            response = jsonify({'order': order.data})
            response.status_code = 201
            return response

        response = jsonify({'Message': "The meal order does not exist"})
        response.status_code = 404
        return response
