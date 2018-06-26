
class Meal(object):
    
    def __init__(self, meal_id, name, price):
        self.id = meal_id
        self.name = name
        self.price = price

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'price': self.price,
        }

    
