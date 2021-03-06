from flask import jsonify, request, abort
from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from app.models import Meal
from app import ma


class MealSchema(ma.Schema):
    
    class Meta:
        fields = ('name', 'price', 'id', 'caterer_id')


meal_schema = MealSchema()
meals_schema = MealSchema(many=True)

'''
    This Meal class implements GET, PUT, DELETE methods for a Meal.
    Authorization for caterer only
'''


class MealResource(Resource):
    "This class handles http operations on a meal resource"

    # Get a single meal option by id
    @jwt_required()
    def get(self, meal_id):
        if not current_identity.is_caterer:
            abort(403,
                  description='You must be an admin to access this resource')

        meal = Meal.query.filter_by(
            id=meal_id,
            caterer_id=current_identity.id).first()
            
        if meal:
            meal_result = meal_schema.dump(meal)
            response = jsonify(meal_result.data)
            response.status_code = 200
            return response
        else:
            response = jsonify({"message": "Meal could not be found."})
            response.status_code = 404
            return response

    # Update the information of a meal option
    @jwt_required()
    def put(self, meal_id):

        if not current_identity.is_caterer:
            abort(403,
                  description='You must be an admin to access this resource')

        request.get_json(force=True)
        meal = Meal.query.filter_by(
            id=meal_id,
            caterer_id=current_identity.id).first()

        if meal:
            meal.name = request.json['name']
            meal.price = request.json['price']
            meal.save()

            response = jsonify(meal_schema.dump(meal).data)
            response.status_code = 200
            return response

        response = jsonify({'Message': 'This meal requested does not exist'})
        response.status_code = 404
        return response

    # Delete a meal option
    @jwt_required()
    def delete(self, meal_id):
        if not current_identity.is_caterer:
            abort(
                403,
                description='You must be an admin to access this resource')
        meal = Meal.query.filter_by(
                id=meal_id).first()
        if meal:
            meal.delete()
            response = jsonify(
                {'result': True, 'message': 'The meal has been deleted'})
            response.status_code = 202
            return response

        response = jsonify({'result': False,
                            'message': 'The meal to delete is not present'})
        response.status_code = 404
        return response


class MealListResource(Resource):
    '''
        This MealList class implements GET, POST methods for Meals.
        Authorization for caterer only
    '''

    # Get all meal options
    @jwt_required()
    def get(self):
        if not current_identity.is_caterer:
            abort(
                403,
                description='You must be an admin to access this resource')

        all_meals = Meal.query.filter_by(
            caterer_id=current_identity.id).all()
        meals = meals_schema.dump(all_meals)
        response = jsonify(meals.data)
        response.status_code = 200
        return response

    # Add a meal option
    @jwt_required()
    def post(self):

        # check for access role
        if not current_identity.is_caterer:
            abort(
                403,
                description='You must be an admin to access this resource')

        request.get_json(force=True)

        # check for missing fields
        if not request.json or 'name' \
                not in request.json or 'price' not in request.json:
            response = jsonify(
                {'Message': 'Missing fields: enter meal name and price'})
            response.status_code = 400
            return response

        meal_name = request.json['name'].strip()

        # check for duplicate meal names
        duplicate = Meal.query.filter_by(name=meal_name).first()
        if duplicate:
            response = jsonify(
                {'Message': 'Duplicate, enter a unique meal name'})
            response.status_code = 409
            return response

        meal_dict = {
            'name': request.json['name'].strip(),
            'price': float(request.json['price'].strip()),
            'caterer_id': current_identity.id
        }

        meal = Meal(
            name=meal_dict['name'],
            price=meal_dict['price'],
            caterer_id=meal_dict['caterer_id'])

        meal.save()
        response = jsonify({'Meal': meal_schema.dump(
            meal).data, 'Message': 'Meal added successfully'})
        response.status_code = 201
        return response
