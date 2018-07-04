from flask import jsonify, request, abort
from flask_restful import Resource
from flask_jwt import JWT, jwt_required, current_identity
from app.entities.meals import Meal
import json

meals_list = [
    Meal(
        1, 'Rice & Chicken', 10.5), Meal(
            2, 'Fries & Beef', 13.5), Meal(
                3, 'Fries & Chicken', 17), Meal(
                    4, 'Potatoes & Beans', 15)]

''' This Meal class implements GET, PUT, DELETE methods for a Meal. Authorization for caterer only'''


class MealResource(Resource):
    "This class handles http operations on a meal resource"

    # Get a single meal option by id
    @jwt_required()
    def get(self, meal_id):
        if not current_identity['is_caterer']:
            response = jsonify(
                {'message': 'You must be an admin to access this resource'})
            response.status_code = 403
            return response

        for meal in meals_list:
            if meal.id == meal_id:
                response = jsonify({'Meal': meal.serialize()})
                response.status_code = 200
                return response

        response = jsonify({'result': False,
                            'message': 'The requested meal does not exist'})
        response.status_code = 404
        return response

    # Update the information of a meal option
    @jwt_required()
    def put(self, meal_id):

        if not current_identity['is_caterer']:
            response = jsonify(
                {'message': 'You must be an admin to access this resource'})
            response.status_code = 403
            return response

        request.get_json(force=True)

        for meal_item in meals_list:
            if meal_item.id == meal_id:
                meal_item.name = request.json['name']
                meal_item.price = request.json['price']
                response = jsonify({'Meal': meal_item.serialize()})
                response.status_code = 200
                return response

        response = jsonify({'Message': 'This meal requested does not exist'})
        response.status_code = 404
        return response

    # Delete a meal option
    @jwt_required()
    def delete(self, meal_id):
        if not current_identity['is_caterer']:
            response = jsonify(
                {'message': 'You must be an admin to access this resource'})
            response.status_code = 403
            return response

        for meal in meals_list:
            if meal.id == meal_id:
                meals_list.remove(meal)
                response = jsonify(
                    {'result': True, 'message': 'The meal has been deleted'})
                response.status_code = 202
                return response

        response = jsonify({'result': False,
                            'message': 'The meal to delete is not present'})
        response.status_code = 404
        return response

    @staticmethod
    def is_duplicate(meal_name):
        for meal in meals_list:
            if meal.name.islower() == meal_name.islower(
            ) and meal.name[1:-1] == meal_name[1:-1]:
                return True
            else:
                continue
        return False


''' This MealList class implements GET, POST methods for Meals. Authorization for caterer only'''


class MealListResource(Resource):

    # Get all meal options
    @jwt_required()
    def get(self):
        if not current_identity['is_caterer']:
            response = jsonify(
                {'message': 'You must be an admin to access this resource'})
            response.status_code = 403
            return response

        response = jsonify(meals=[meal.serialize() for meal in meals_list])
        response.status_code = 200
        return response

    # Add a meal option
    @jwt_required()
    def post(self):
        if not current_identity['is_caterer']:
            response = jsonify(
                {'message': 'You must be an admin to access this resource'})
            response.status_code = 403
            return response

        request.get_json(force=True)
        if not request.json or 'name' not in request.json or 'price' not in request.json:
            abort(400)

        meal_name = request.json['name'].strip()
        if MealResource.is_duplicate(meal_name):
            response = jsonify(
                {'Message': 'Duplicate, enter a unique meal name', 'Status code': '409'})
            response.status_code = 409
            return response

        meal_dict = {
            'id': int(meals_list[-1].id + 1),
            'name': request.json['name'].strip(),
            'price': float(request.json['price'].strip())
        }

        meal = Meal(meal_dict['id'], meal_dict['name'], meal_dict['price'])
        meals_list.append(meal)
        response = jsonify(
            {'Meal': meal.serialize(), 'Message': 'Meal added successfully'})
        response.status_code = 201
        return response

    @classmethod
    def get_meals_by_id(cls, meal_id):
        meal = None
        for meal_item in meals_list:
            if meal_item.id == meal_id:
                meal = meal_item.serialize()
        return meal

    def restricted(self):
        if not current_identity['is_caterer']:
            response = jsonify(
                {'message': 'You must be an admin to access this resource'})
            response.status_code = 403
            return response
        else:
            return None
