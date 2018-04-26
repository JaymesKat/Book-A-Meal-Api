from flask_restful import Resource
from api.resources.meals import Meal

class Menu(Resource):

    menu = [
         {
            'meal_ids': [1,2,3,4]
        }
    ]

    def get_menu_list(self):
        menu = {}
        menu['meals'] = Meal.get_menu_list(self.menu['meal_ids'])
        return menu

    def post(self):
        pass