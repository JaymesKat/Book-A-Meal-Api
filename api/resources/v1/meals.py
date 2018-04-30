from flask import  jsonify, request, abort, make_response
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


    # CRUD operations

    # Get all meal options
    def get(self):
        return jsonify({'meals': self.meals})

    # Get meal option by id
    def get(self, meal_id):
        for meal_item in self.meals:
            if meal_item['id'] == meal_id:
                meal = meal_item
        return jsonify({'Meal': meal}, 200)        

    # Add a meal option
    def post(self):        
        new_meal = self.meals[self.meals[-1]['id'] + 1]
        new_meal = request.json['data']
        return jsonify({'Meal': new_meal}, 201)

    # Update the information of a meal option
    def put(self, meal_id):
        self.meals[meal_id] = request.json['data']
        return jsonify({'Meal': self.meals[meal_id]}, 204)

    # Delete a meal option
    def delete(self, meal_id):
        meal_to_delete = [meal for meal in self.meals if meal['id'] == meal_id]
        if not meal_to_delete:
            abort(404)
        self.meals.remove(meal_to_delete)
        return jsonify({'result': True}, 204)