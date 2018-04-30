from flask import  jsonify, request, abort
from flask_restful import Resource
from api.resources.meals import Meal

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
        new_menu = request.json['data']
        return jsonify({'Menu': new_menu})

    # Update menu for the day
    def put(self):       
        pass 
        