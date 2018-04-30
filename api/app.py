# Entry point for flask app
import datetime
from flask import Flask, Blueprint
from flask_restful import Api
from api import create_app

from api.resources.v1.meals import Meal
from api.resources.v1.orders import Order
from api.resources.v1.menu import Menu
from api.resources.v1.user import User

app = create_app('development_env')
api = Api(app)

api.add_resource(User, 
    '/api/v1/auth/register',
    '/api/v1/auth/login')

api.add_resource(Order, 
    '/api/v1/orders/',
    '/api/v1/orders/<int:orderId>')

api.add_resource(Meal, 
    '/api/v1/meals/',
    '/api/v1/meals/<int:mealId>')

api.add_resource(Menu, '/api/v1/menu/')

