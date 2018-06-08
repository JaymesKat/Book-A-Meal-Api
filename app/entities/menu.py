import datetime
from app.resources.v1.meals import MealListResource

class Menu(object):
    
    def __init__(self, meal_list):
        self.meal_list = meal_list
        self.date_submitted = datetime.date.today().strftime("%Y-%m-%d")

    def serialize(self):
        return {
            'meals': [MealListResource.get_meals_by_id(meal)for meal in self.meal_list]
        }