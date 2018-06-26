import json
from flask import jsonify, request, abort
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from app.models import Meal
from app import ma

class MealSchema(ma.Schema):
    class Meta:
        model = Meal

# meals_list = [ Meal('Rice & Chicken',10.5),Meal('Fries & Beef',13.5),Meal('Fries & Chicken',17), Meal('Potatoes & Beans',15)]

meal_schema = MealSchema()
meals_schema = MealSchema(many=True)

''' This Meal class implements GET, PUT, DELETE methods for a Meal. Authorization for caterer only'''
class MealResource(Resource):
    "This class handles http operations on a meal resource"

    # Get a single meal option by id
    @jwt_required()
    def get(self, meal_id):
        if current_identity['is_caterer'] == False:
            response = jsonify({'message':'You must be an admin to access this resource'})
            response.status_code = 403
            return response

        try:
            meal = Meal.query.get(meal_id)
        except IntegrityError:
            response = jsonify({"message": "Meal could not be found."})
            response.status_code = 400
            return response

        meal_result = meal_schema.dump(meal)
        response = {"Meal": meal_result.data}
        response.status_code = 200
        return response

    # Update the information of a meal option
    @jwt_required()
    def put(self, meal_id):

        if current_identity['is_caterer'] == False:
            response = jsonify({'message':'You must be an admin to access this resource'})
            response.status_code = 403
            return response

        request.get_json(force=True)
        meal = Meal.query.get(meal_id)
        if meal: 
            meal.name = request.json['name']
            meal.price = request.json['price']
            meal.save()

            response = jsonify({'Meal updated': meal_schema.dump(meal).data}) 
            response.status_code = 200
            return response
        
        response = jsonify({'Message': 'This meal requested does not exist'})
        response.status_code = 404
        return response

    # Delete a meal option
    @jwt_required()
    def delete(self, meal_id):
        if current_identity['is_caterer'] == False:
            response = jsonify({'message':'You must be an admin to access this resource'})
            response.status_code = 403
            return response

        meal = Meal.query.get(meal_id)
        if meal: 
            meal.delete()
            response = jsonify({'result': True, 'message':'The meal has been deleted'})
            response.status_code = 202
            return response

        response = jsonify({'result': False,'message':'The meal to delete is not present'})
        response.status_code = 404
        return response
        

    @staticmethod
    def is_duplicate(meal_name):
        meals = Meal.query.all()
        for meal in meals:
            if meal.name.islower() == meal_name.islower() and meal.name[1:-1] == meal_name[1:-1]:
                return True
            else:
                continue
        return False

''' This MealList class implements GET, POST methods for Meals. Authorization for caterer only'''
class MealListResource(Resource):

    # Get all meal options
    @jwt_required()
    def get(self):
        if current_identity['is_caterer'] == False:
            response = jsonify({'message':'You must be an admin to access this resource'})
            response.status_code = 403
            return response
        all_meals = Meal.query.all()
        meals = meals_schema.dump(all_meals)
        response = jsonify({'meals':meals})
        response.status_code = 200
        return response

    # Add a meal option
    @jwt_required()
    def post(self):
        if current_identity['is_caterer'] == False:
            response = jsonify({'message':'You must be an admin to access this resource'})
            response.status_code = 403
            return response

        request.get_json(force=True)
        if not request.json or not 'name' in request.json or not 'price' in request.json:
            abort(400)

        meal_name = request.json['name'].strip()
        if MealResource.is_duplicate(meal_name):
            response = jsonify({'Message':'Duplicate, enter a unique meal name','Status code': '409'})
            response.status_code = 409
            return response
            
        meal_dict = {
            'name': request.json['name'].strip(),
            'price': float(request.json['price'].strip())
        }

        meal = Meal(meal_dict['name'],meal_dict['price'])
        meal.save()
        response = jsonify({'Meal': meal_schema.dump(meal), 'Message': 'Meal added successfully'})
        response.status_code = 201
        return response