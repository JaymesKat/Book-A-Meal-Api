from flask import jsonify, request, abort
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource
from app.resources.v1.meals import MealResource, MealListResource
from app.models import Menu, Meal
from app import ma

class MenuSchema(ma.Schema):
    class Meta:
        model = Menu

''' This Menu class implements GET and POST methods for a Meal. Authorization for both customer and caterer'''
menu_schema = MenuSchema()
class MenuResource(Resource):

    daily_menu = Menu([4, 1, 3, 2])

    # CRUD operations
    # Get menu for the day
    @jwt_required()
    def get(self):
        menu = Menu.query.order_by('updated desc').first()     
        response = jsonify({'Today\'s menu': menu_schema.dump(menu)})
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
        meal_ids = request.json['meal_ids']

        menu = Menu()
        for meal_id in meal_ids:
            if isinstance(meal_id,int):
                menu.items.append(Meal.query.get(meal_id))
        menu.save()       
        
        response = jsonify({'Menu': menu_schema.dump(menu)})
        response.status_code = 201
        return response
