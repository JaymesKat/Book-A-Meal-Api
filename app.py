import datetime
from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api
from api.resources.users import User
from api.resources.menu import Menu
from api.resources.orders import Order
from api.resources.meals import Meal
# from flask_sqlalchemy import SQLAlchemy

from api import create_app

app =  Flask(__name__)

#Sign up a user
@app.route('/api/v1/auth/login', methods=['POST'])
def signup():
    pass

#Login a user
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    pass

# Get all meal options
@app.route('/api/v1/meals/', methods=['GET'])
def get_all_meals():
    return jsonify({'meals': Meal.meals})

# Add a meal option
@app.route('/api/v1/meals/', methods=['POST'])
def add_meal():
    if not request.json or not 'name' in request.json or not 'price' in request.json:
        abort(400)
    meal = {
        'id': Meal.meals[-1]['id'] + 1,
        'name': request.json['name'],
        'price': request.json.get['price']
    }
    Meal.add(meal)
    return jsonify({'meal': meal}), 201

# Update the information of a meal option
@app.route('/api/v1/meals/<mealId>', methods=['PUT'])
def update_meal(meal_id):
    meal = [meal for meal in Meal.meals if meal['id'] == meal_id]
    if len(order) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' not in request.json or 'price' not in request.json :
        abort(400)

    meal[0]['name'] = request.json.get('name', order[0]['name'])
    meal[0]['price'] = request.json.get('price', order[0]['price'])
    return jsonify({'meal': meal[0]})

# Remove a meal option
@app.route('/api/v1/meals/<mealId>', methods=['DELETE'])
def delete_meal(meal_id):
    meal = [meal for meal in Meal.meals if meal['id'] == meal]
    if len(meal) == 0:
        abort(404)
    Meal.meals.remove(meal[0])
    return jsonify({'result': True})

# Get menu for the day
@app.route('/api/v1/menu/', methods=['GET'])
def get_menu():
    return jsonify({'menu': Menu.get_meals_on_menu(Menu)})

# Setup menu for the day
@app.route('/api/v1/menu/', methods=['POST'])
def set_menu():
    return jsonify({'menu': Menu.get_meals_on_menu(Menu)})

# Get all orders
@app.route('/api/v1/orders/', methods=['GET'])
def get_orders():
    return jsonify({'orders': Order.orders})

# Select meal option from the menu
@app.route('/api/v1/orders', methods=['POST'])
def add_order():
    if not request.json or not 'meals' in request.json:
        abort(400)
    meal = {
        'id': Order.orders[-1]['id'] + 1,
        'meals': request.json['meals'],
        'date_submitted': datetime.date.today().strftime("%Y-%m-%d")
    }
    Meal.add(meal)
    return jsonify({'meal': meal}), 201

# Modify an order
@app.route('/api/v1/orders/<orderId>', methods=['PUT'])
def update_order(order_id):
    order = [order for order in Order.orders if order['id'] == order_id]
    if len(order) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'meals' not in request.json:
        abort(400)
    
    order[0]['meals'] = request.json.get('meals', order[0]['meals'])
    return jsonify({'order': order[0]})

# Delete an order
@app.route('/api/v1/orders/<order_id>', methods=['DELETE'])
def delet_order(order_id):
    order = [order for order in Order.orders if order['id'] == order]
    if len(order) == 0:
        abort(404)
    Order.orders.remove(order[0])
    return jsonify({'result': True})

   

if __name__ == '__main__':
    app.run(debug=True)