from flask import  jsonify, request, abort
from flask_restful import Resource
from api.resources.v1.meals import Meal

class Menu(Resource):

    menu =  {
            'meal_ids': [4,1,3,2]
        }

    # CRUD operations

    # Get menu for the day
    def get(self):
        meals = []
        for id in self.menu['meal_ids']:
            meals.append(Meal.get(Meal,id))
        return jsonify({'menu': self.menu})

    # Create menu for the day
    def post(self):
        request.get_json(force=True)
        self.menu['meal_ids']  =  request.json['meal_ids']
        response = jsonify({'Menu': self.menu})
        response.status_code = 201
        return response

    # Update menu for the day
    def put(self):       
        pass 
        