from flask import jsonify, request, abort
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource
from api.resources.v1.meals import Meal, MealList

''' This Menu class implements GET and POST methods for a Meal. Authorization for both customer and caterer'''

class Menu(Resource):

    menu = {
        'meal_ids': [4, 1, 3, 2]
    }

    # CRUD operations
    # Get menu for the day
    @jwt_required()
    def get(self):
        meals = []
        for meal_id in self.menu['meal_ids']:
            meals.append(MealList.get_meals_by_id(meal_id))
        response = jsonify({'menu': meals})
        response.status_code = 200
        return response

    # Create menu for the day by caterer
    @jwt_required()
    def post(self):
        if current_identity['is_caterer'] == False:
            response = jsonify({'message':'You must be an admin to access this resource'})
            response.status_code = 401
            return response  
                  
        request.get_json(force=True)
        self.menu['meal_ids'] = request.json['meal_ids']
        response = jsonify({'Menu': self.menu})
        response.status_code = 201
        return response

    # Update menu for the day
    def put(self):
        pass
