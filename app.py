from flask import Flask, jsonify, abort
from flask_restful import Resource, Api
from api.resources.users import User
from api.resources.menu import Menu
from api.resources.orders import Order
from api.resources.meals import Meal
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/api/v1/auth/login', methods=['POST'])
def authenticate():
    pass

@app.route('/api/v1/meals', methods=['GET'])
def get_all_meals():
    return jsonify({'meals': Meal.meals})

@app.route('/api/v1/menu', methods=['GET'])
def get_menu():
    return jsonify({'menu': Menu.menu})

@app.route('/api/v1/orders', methods=['GET'])
def get_orders():
    return jsonify({'orders': Order.orders})

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run()