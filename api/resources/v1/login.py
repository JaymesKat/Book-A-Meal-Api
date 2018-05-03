import datetime
from flask import request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource
from api.resources.v1.users import User

''' This method handles user authentication and authorization ''' 
class Login(Resource):

    @staticmethod
    def authenticate(email, password):
        # Check if user is found in records
        user = User.get_user(email, password)
        return user

    @staticmethod
    def identity(payload):
        user_email = payload['identity']
        return User.get_user(user_email, None)

           
    @staticmethod   
    @jwt_required
    def post():
        response = jsonify({"authorization": current_identity})
        response.status_code = 200
        return response

    @staticmethod
    def log_out():
        pass    