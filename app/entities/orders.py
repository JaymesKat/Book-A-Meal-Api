import datetime
from app.resources.v1.meals import MealListResource

class Order(object):
    
    def __init__(self, order_id,meal_id, user_id):
        self.id = order_id
        self.meal_id = meal_id
        self.date_submitted = datetime.date.today().strftime("%Y-%m-%d")
        self.user_id = user_id
        self.completed = False

    def serialize(self):
        return {
            'id': self.id,
            'meal': MealListResource.get_meals_by_id(self.meal_id),
            'date_submitted': self.date_submitted,
            'submitted_by': 'User ID: '+str(self.user_id),
            'completed': self.completed
        }