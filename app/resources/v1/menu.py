from flask import jsonify, request, abort
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource
from app.resources.v1.meals import MealResource, MealListResource, MealSchema
from app.models import Menu, Meal
from app import ma


class MenuSchema(ma.Schema):
    class Meta:
        fields = ("date_created", "items")
    items = ma.List(ma.HyperlinkRelated('meal_detail'))


menu_schema = MenuSchema()
meals_schema = MealSchema(many=True)
meal_schema = MealSchema()



class MenuResource(Resource):
    ''' This Menu class implements GET and POST methods for a Menu. Authorization for both customer and caterer'''

    # Get menu for the day
    @jwt_required()
    def get(self):
        menu = Menu.query.order_by('date_created').first()

        meal_ids = [meal.id for meal in menu.items]
        menu_meals = meals_schema.dump(menu.items)

        response = jsonify(
            {"meals on menu": menu_meals.data, "meal_ids": meal_ids})
        response.status_code = 200
        return response

    # Create menu for the day by caterer
    @jwt_required()
    def post(self):
        if not current_identity.is_caterer:
            response = jsonify(
                {'message': 'You must be an admin to access this resource'})
            response.status_code = 403
            return response

        request.get_json(force=True)
        meal_ids = request.json['meal_ids']

        menu = Menu()
        for meal_id in meal_ids:
            menu.items.append(Meal.query.get(meal_id))
        menu.save()

        meal_ids = [meal.id for meal in menu.items]
        menu_meals = meals_schema.dump(menu.items)

        response = jsonify(
            {"meals on menu": menu_meals.data, "meal_ids": meal_ids})
        response.status_code = 201
        return response
