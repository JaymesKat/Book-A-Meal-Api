import datetime
from flask import jsonify, request, abort
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource
from app.resources.v1.meals import MealSchema
from app.models import Menu, Meal, Day, User
from app import ma
from app.resources.v1.auth import UserSchema


class DaySchema(ma.Schema):

    class Meta:
        fields = ('id', 'name')


class MenuSchema(ma.Schema):

    caterer = ma.Nested(UserSchema)

    class Meta:
        fields = ("date_created", "items", "day_id", "caterer_id", "caterer")


menus_schema = MenuSchema(many=True)
day_schema = DaySchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
meal_schema = MealSchema()
meals_schema = MealSchema(many=True)


class MenuResource(Resource):
    '''
        This Menu class implements GET and POST methods for a Menu.
        Authorization for both customer and caterer
    '''

    # Get menus
    @jwt_required()
    def get(self):
        if current_identity.is_caterer:
            full_menus = []
            menus = Menu.query.filter_by(
                        caterer_id=current_identity.id).order_by(
                        Menu.day_id.asc(),
                        Menu.date_created.desc())\
                        .distinct('day_id').limit(7).all()

            for menu in menus:
                full_menus.append(get_menu_dict(menu))

            response = jsonify(full_menus)
            response.status_code = 200
            return response

        else:
            caterers = User.query.filter_by(is_caterer=True).all()
            caterers_with_menus = []
            today_id = datetime.datetime.today().weekday()+1
            for caterer in caterers:
                menu = Menu.query.filter_by(
                        caterer_id=caterer.id,
                        day_id=today_id)\
                        .order_by(
                        Menu.date_created.desc()).first()
                
                caterer_menu = get_menu_dict(menu)

                caterer_dict = {}
                caterer_dict['caterer'] = user_schema.dump(caterer).data
                caterer_dict['menuDetails'] = caterer_menu
                caterers_with_menus.append(caterer_dict)

            response = jsonify(caterers_with_menus)
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
        if 'day' in request.json.keys():
            day_id = request.json['day']
        else:
            day_id = datetime.datetime.today().weekday()+1

        menu = Menu()
        menu.day_id = day_id
        menu.caterer_id = current_identity.id

        for meal_id in meal_ids:
            if not str(meal_id).isdigit():
                abort(400, description="Invalid meal id has been entered")

            meal = Meal.query.filter_by(
                        id=int(meal_id),
                        caterer_id=current_identity.id).first()
            if meal:
                menu.items.append(meal)
        menu.save()
        menu_dict = get_menu_dict(menu)

        response = jsonify(menu_dict)
        response.status_code = 201
        return response

    @jwt_required()
    def put(self):
        if not current_identity.is_caterer:
            abort(
                403,
                description="You must be an admin to access this resource")

        request.get_json(force=True)
        if 'day' not in request.json.keys():
            day_id = datetime.datetime.today().weekday()+1
        else:
            day_id = request.json['day']

        menu = Menu.query.filter_by(
                    day_id=day_id,
                    caterer_id=current_identity.id).order_by('date_created desc').first()
        if not menu:
            menu = Menu(day_id=day_id)
        menu.items = []

        # Get list of meal ids removing duplicates
        meal_ids = list(set(request.json['meal_ids']))
        for meal_id in meal_ids:
            if not isinstance(meal_id, int):
                abort(400, description="Invalid meal id has been entered")

            meal = Meal.query.filter_by(
                        id=meal_id,
                        caterer_id=current_identity.id).first()
            if meal:
                menu.items.append(meal)

        menu.date_created = datetime.datetime.utcnow()
        menu.save()

        updated_menu = get_menu_dict(menu)
        updated_menu['Message'] = "Menu updated"

        response = jsonify(updated_menu)

        response.status_code = 201
        return response


class MenuSingleResource(Resource):
    
    # Get menu for a particular day
    @jwt_required()
    def get(self, day_id):
        caterer_id = current_identity.id
        menu = Menu.query.filter_by(
                    caterer_id=caterer_id,
                    day_id=day_id).order_by('date_created desc').first()
        if not menu:
            abort(400, description="Menu does not exist")

        menu_dict = get_menu_dict(menu)
        response = jsonify(menu_dict)
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

        updated_menu = get_menu_dict(menu)
        updated_menu['Message'] = "Menu updated"
        response = jsonify(updated_menu)

        response.status_code = 201
        return response


def get_menu_dict(menu):
    if menu:
        mealIds = [meal.id for meal in menu.items]
        mealList = meals_schema.dump(menu.items).data
        day = day_schema.dump(Day.query.get(menu.day_id))
        date_created = menu.date_created
    else:
        today_id = datetime.datetime.today().weekday()+1
        mealIds = []
        mealList = []
        day = day_schema.dump(Day.query.get(today_id))
        date_created = ""

    menu_dict = {
        "day": day.data,
        "mealIds": mealIds,
        "mealList": mealList,
        "dateCreated": date_created
    }

    return menu_dict
