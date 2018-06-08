# Entry point for flask app
import datetime
from flask import Flask, render_template, make_response
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource
from resources.v1.meals import MealResource, MealListResource
from resources.v1.orders import OrderResource, OrderListResource
from resources.v1.menu import MenuResource
from resources.v1.registration import RegistrationResource
from resources.v1.login import LoginResource

class Home(Resource):
    
    def get(self):
        ''' Index route '''
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)

def setup_routes(api):

    api.add_resource(Home, '/')

    api.add_resource(RegistrationResource,'/api/v1/auth/register/')

    api.add_resource(OrderListResource, '/api/v1/orders/')
    api.add_resource(OrderResource, '/api/v1/orders/<int:order_id>')

    api.add_resource(MealListResource, '/api/v1/meals/')
    api.add_resource(MealResource, '/api/v1/meals/<int:meal_id>')

    api.add_resource(MenuResource, '/api/v1/menu/')


