
class Meal(object):
    
    def __init__(self, meal_id, name, price):
        self.id = meal_id
        self.name = name
        self.price = price


    '''Add a new meal'''
    def save(self, id, name, price):
        pass

    '''Get a meal by id'''
    def get_by_id(self, id):
        pass
        
    '''Get list of all meals'''
    def get(self):
        pass

    '''Update a meal'''
    def update(self, id, name,price):
        pass

    '''Delete a meal'''
    def delete(self):
        pass

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'price': self.price,
        }

    
