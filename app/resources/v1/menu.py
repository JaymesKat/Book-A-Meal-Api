import datetime
from flask import jsonify, request, abort
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource
from app.resources.v1.meals import MealSchema
from app.models import Menu, Meal, Day
from app import ma


class DaySchema(ma.Schema):

    class Meta:
        fields = ('id', 'name')


class MenuSchema(ma.Schema):

    class Meta:
        fields = ("date_created", "items", "day_id")


menus_schema = MenuSchema(many=True)
day_schema = DaySchema()
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
        menus = Menu.query.order_by(
                    Menu.day_id.asc(),
                    Menu.date_created.desc()).distinct('day_id').limit(7).all()
        full_menus = []
        for menu in menus:
            mealIds = [meal.id for meal in menu.items]
            mealList = meals_schema.dump(menu.items)
            day = day_schema.dump(Day.query.get(menu.day_id))
            
            full_menus.append({
                "day": day.data,
                "mealIds": mealIds,
                "mealList": mealList.data,
                "dateCreated": menu.date_created
            })

        response = jsonify(full_menus)
        response.status_code = 200
        return response

    # Create menu for the day by caterer
    @jwt_required()
    def post(self):
        if not current_identity.is_caterer:
            abort(
                403,
                description="You must be an admin to access this resource")

        request.get_json(force=True)
        
        # Get list of meal ids removing duplicates
        meal_ids = list(set(request.json['meal_ids']))
        day_id = request.json['day']

        menu = Menu()
        menu.day_id = day_id

        for meal_id in meal_ids:
            if not isinstance(meal_id, int):
                abort(400, description="Invalid meal id has been entered")

            if Meal.query.get(meal_id):
                menu.items.append(Meal.query.get(meal_id))
        menu.save()

        meal_ids = [meal.id for meal in menu.items]
        menu_meals = meals_schema.dump(menu.items)
        day = Day.query.get(menu.day_id)
        day = day_schema.dump(day)

        response = jsonify(
            {
                "day": day.data,
                "mealList": menu_meals.data,
                "mealIds": meal_ids,
                "date_created": menu.date_created
            })
        response.status_code = 201
        return response

    @jwt_required()
    def put(self):
        request.get_json(force=True)
        if 'day' not in request.json.keys():
            day_id = datetime.datetime.today().weekday()+1
        else:
            day_id = request.json['day']

        menu = Menu.query.filter_by(
                    day_id=day_id).order_by('date_created desc').first()
        if not menu:
            menu = Menu(day_id=day_id)
        menu.items = []

        # Get list of meal ids removing duplicates
        meal_ids = list(set(request.json['meal_ids']))
        for meal_id in meal_ids:
            if not isinstance(meal_id, int):
                abort(400, description="Invalid meal id has been entered")

            if Meal.query.get(meal_id):
                menu.items.append(Meal.query.get(meal_id))

        menu.date_created = datetime.datetime.utcnow()
        menu.save()

        meal_ids = [meal.id for meal in menu.items]
        menu_meals = meals_schema.dump(menu.items)

        day = Day.query.get(menu.day_id)
        day = day_schema.dump(day)

        response = jsonify(
            {
                "Message": "Menu updated",
                "day": day.data,
                "mealList": menu_meals.data,
                "mealIds": meal_ids,
                "date_created": menu.date_created
            }
        )

        response.status_code = 201
        return response


class MenuSingleResource(Resource):
    
    # Get menu for a particular day
    @jwt_required()
    def get(self, day_id):
        menu = Menu.query.filter_by(
                    day_id=day_id).order_by('date_created desc').first()
        if not menu:
            abort(400, description="Menu does not exist")

        meal_ids = [meal.id for meal in menu.items]
        menu_meals = meals_schema.dump(menu.items)

        day = Day.query.get(menu.day_id)
        day = day_schema.dump(day)

        response = jsonify(
            {
                "day": day.data,
                "mealList": menu_meals.data,
                "mealIds": meal_ids,
                "date_created": menu.date_created
            }
        )

        response.status_code = 200
        return response

    # Edit menu for the day
    @jwt_required()
    def put(self, day_id):
        menu = Menu.query.filter_by(
                    day_id=day_id).order_by('date_created desc').first()
        if not menu:
            abort(400, description="Menu does not exist")
                
        menu.items = []

        # Get list of meal ids removing duplicates
        meal_ids = list(set(request.json['meal_ids']))
        for meal_id in meal_ids:
            if not isinstance(meal_id, int):
                abort(400, description="Invalid meal id has been entered")

            if Meal.query.get(meal_id):
                menu.items.append(Meal.query.get(meal_id))
        
        menu.date_created = datetime.datetime.utcnow()
        menu.save()

        meal_ids = [meal.id for meal in menu.items]
        menu_meals = meals_schema.dump(menu.items)

        day = Day.query.get(menu.day_id)
        day = day_schema.dump(day)

        response = jsonify(
            {
                "Message": "Menu updated",
                "day": day.data,
                "mealList": menu_meals.data,
                "mealIds": meal_ids,
                "date_created": menu.date_created
            }
        )

        response.status_code = 201
        return response
