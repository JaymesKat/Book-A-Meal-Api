from flask import jsonify, request, abort
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource
from app.resources.v1.meals import MealSchema
from app.models import Menu, Meal
from app import ma


class MenuSchema(ma.Schema):
    class Meta:
        fields = ("date_created", "items")


menu_schema = MenuSchema()
meals_schema = MealSchema(many=True)
meal_schema = MealSchema()


class MenuResource(Resource):
    '''
        This Menu class implements GET and POST methods for a Menu.
        Authorization for both customer and caterer
    '''

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
            abort(
                403,
                description="You must be an admin\
                to access this resource")

        request.get_json(force=True)
        meal_ids = request.json['meal_ids']

        menu = Menu()
        for meal_id in meal_ids:
            if not isinstance(meal_id, int):
                abort(400, description="Invalid meal id has been entered")

            if Meal.query.get(meal_id):
                menu.items.append(Meal.query.get(meal_id))
        menu.save()

        meal_ids = [meal.id for meal in menu.items]
        menu_meals = meals_schema.dump(menu.items)

        response = jsonify(
            {"meals on menu": menu_meals.data, "meal_ids": meal_ids})
        response.status_code = 201
        return response

    @jwt_required()
    def put(self):
        menu = Menu.query.order_by('date_created').first()

        menu.items = []

        meal_ids = request.json['meal_ids']
        for meal_id in meal_ids:
            if not isinstance(meal_id, int):
                abort(400, description="Invalid meal id has been entered")

            if Meal.query.get(meal_id):
                menu.items.append(Meal.query.get(meal_id))
        menu.save()

        meal_ids = [meal.id for meal in menu.items]
        menu_meals = meals_schema.dump(menu.items)

        response = jsonify(
            {
                "Message": "Menu updated",
                "meals on menu": menu_meals.data,
                "meal_ids": meal_ids
            }
        )

        response.status_code = 201
        return response
