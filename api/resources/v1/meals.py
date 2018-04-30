from flask import  jsonify, request, abort
from flask_restful import Resource

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

class Meal(Resource):

    # CRUD operations

    # Get meal option by id
    def get(self, meal_id):
        for meal_item in meals:
            if meal_item['id'] == meal_id:
                meal = meal_item
        return jsonify({'Meal': meal}, 200)        

    # Update the information of a meal option
    def put(self, meal_id):
        request.get_json(force=True)
        meal_to_update = [meal for meal_item in meals if meal_item['id'] == meal_id]
        meal_to_update = request.data
        response = jsonify({'Meal': meal_to_update})
        response.status_code = 204
        return response

    # Delete a meal option
    def delete(self, meal_id):
        meal_to_delete = [meal for meal in meals if meal['id'] == meal_id]
        if not meal_to_delete:
            abort(404)
        meals.remove(meal_to_delete)
        return jsonify({'result': True}, 204)

class MealList(Resource):
    
    # CRUD operations

    # Get all meal options
    def get(self):
        response = jsonify({'meals': meals})
        response.status_code = 200
        return response

    # Add a meal option
    def post(self): 
        request.get_json(force=True)
        if not request.json or not 'name' in request.json:
            abort(400)

        meal = {    
            'id': int(meals[-1]['id'] + 1),
            'name' : request.json['name'],
            'price' : float(request.json['price'].strip())
        } 
        meals.append(meal)
        response = jsonify({'Meal': meal})
        response.status_code = 201
        return response