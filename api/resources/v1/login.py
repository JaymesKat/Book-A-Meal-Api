import datetime
from flask import request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource
from api.resources.v1.users import User

''' This method handles user authentication and authorization ''' 
class Login(Resource):

    @staticmethod
    def authenticate(email, password):
        user = User.get_user(email, password)
        return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        return User.get_user_by_id(user_id)
