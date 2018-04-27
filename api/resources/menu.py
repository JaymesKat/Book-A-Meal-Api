from flask_restful import Resource
from api.resources.meals import Meal

class Menu(Resource):

    menu =  {
            'meal_ids': [4,1,3,2]
        }

    def get_meals_on_menu(self):
        meals = []
        for id in self.menu['meal_ids']:
            meals.append(Meal.get_meal(Meal,id))
        return meals

    def add(self, meal_id):
        self.menu['meal_ids'].append(meal_id)