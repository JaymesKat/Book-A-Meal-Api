from flask import jsonify, request, abort
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource
from app.resources.v1.meals import MealResource, MealListResource
from app.entities.menu import Menu

''' This Menu class implements GET and POST methods for a Meal. Authorization for both customer and caterer'''

class MenuResource(Resource):

    daily_menu = Menu([4, 1, 3, 2])

    # CRUD operations
    # Get menu for the day
    @jwt_required()
    def get(self):
        meals = []
        for meal_id in self.daily_menu.meal_list:
            meals.append(MealListResource.get_meals_by_id(meal_id))
        response = jsonify({'menu': meals})
        response.status_code = 200
        return response

    # Create menu for the day by caterer
    @jwt_required()
    def post(self):
        if current_identity['is_caterer'] == False:
            response = jsonify({'message':'You must be an admin to access this resource'})
            response.status_code = 403
            return response  
                  
        request.get_json(force=True)
        self.daily_menu = Menu(request.json['meal_ids'])
        response = jsonify({'Menu': self.daily_menu.serialize()})
        response.status_code = 201
        return response

    # Update menu for the day
    def put(self):
        pass
