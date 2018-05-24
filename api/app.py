# Entry point for flask app
import datetime
from flask import Flask, render_template
from flask_jwt import JWT, jwt_required, current_identity
from api.resources.v1.meals import Meal, MealList
from api.resources.v1.orders import Order, OrderList
from api.resources.v1.menu import Menu
from api.resources.v1.registration import Registration
from api.resources.v1.login import Login


def setup_routes(api):

    api.add_resource(Home, '/')

    api.add_resource(Registration,'/api/v1/auth/register/')
    api.add_resource(Login, '/api/v1/auth/login/')

    api.add_resource(OrderList, '/api/v1/orders/')
    api.add_resource(Order, '/api/v1/orders/<int:order_id>')

    api.add_resource(MealList, '/api/v1/meals/')
    api.add_resource(Meal, '/api/v1/meals/<int:meal_id>')

    api.add_resource(Menu, '/api/v1/menu/')

class Home(object):

    def get(self):
        ''' Index route '''
        return render_template('index.html')
