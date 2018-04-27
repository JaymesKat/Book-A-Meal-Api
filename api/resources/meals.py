from flask_restful import Resource

class Meal(Resource):

    meals = [
        {
            'id': 1,
            'name': u'Rice & Chicken',
            'price': 10.5
        },
        {
            'id': 2,
            'name': u'Fries & Beef',
            'price': 13.5
        },
        {
            'id': 3,
            'name': u'Fries & Chicken',
            'price': 17
        },
        {
            'id': 4,
            'name': u'Potatoes & Beans',
            'price': 15
        }
    ]

    def get_meal(self, meal_id):
        for meal in self.meals:
            if meal['id'] == meal_id:
                return meal
        

    def add(self, meal):
        self.meals.append(meal)