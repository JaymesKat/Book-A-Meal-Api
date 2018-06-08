import datetime
from flask import request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource
from app.resources.v1.users import UserResource

''' This method handles user authentication and authorization ''' 
class LoginResource(Resource):

    @staticmethod
    def authenticate(email, password):
        user = UserResource.get_user(email, password)
        return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        return UserResource.get_user_by_id(user_id)
