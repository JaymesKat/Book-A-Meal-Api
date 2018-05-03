from flask import jsonify, request, abort
from flask_restful import Resource
from flask_jwt import JWT, jwt_required
import json

meals = [
    {
        'id': 1,
        'name': 'Rice & Chicken',
        'price': 10.5
    },
    {
        'id': 2,
        'name': 'Fries & Beef',
        'price': 13.5
    },
    {
        'id': 3,
        'name': 'Fries & Chicken',
        'price': 17
    },
    {
        'id': 4,
        'name': 'Potatoes & Beans',
        'price': 15
    }
]

''' This Meal class implements GET, PUT, DELETE methods for a Meal. Authorization for caterer only'''
class Meal(Resource):

    # CRUD operations

    # Get a single meal option by id
    @jwt_required()
    def get(self, meal_id):
        meal = [meal_item for meal_item in meals if meal_item['id'] == meal_id]
        if not meal:
            abort(404)

        return jsonify({'Meal': meal}, 200)

    # Update the information of a meal option
    @jwt_required()
    def put(self, meal_id):
        request.get_json(force=True)

        meal_to_update = [
            meal_item for meal_item in meals if meal_item['id'] == meal_id]
        meal_to_update[0]['name'] = request.json['name']
        meal_to_update[0]['price'] = request.json['price']

        response = jsonify({'Meal': meal_to_update[0]})
        response.status_code = 200
        return response

    # Delete a meal option
    @jwt_required()
    def delete(self, meal_id):
        meal_to_delete = [meal for meal in meals if meal['id'] == meal_id]
        if not meal_to_delete:
            abort(404)

        meals.remove(meal_to_delete[0])
        return jsonify({'result': True}, 204)


''' This MealList class implements GET, POST methods for Meals. Authorization for caterer only'''
class MealList(Resource):

    # Get all meal options
    @jwt_required()
    def get(self):
        response = jsonify({'meals': meals})
        response.status_code = 200
        return response

    # Add a meal option
    @jwt_required()
    def post(self):
        request.get_json(force=True)
        if not request.json or not 'name' in request.json or not 'price' in request.json:
            abort(400)

        meal = {
            'id': int(meals[-1]['id'] + 1),
            'name': request.json['name'],
            'price': float(request.json['price'].strip())
        }
        meals.append(meal)
        response = jsonify({'Meal': meal})
        response.status_code = 201
        return response
