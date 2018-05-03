import datetime
from flask import request, jsonify
from flask_jwt import JWT, jwt_required
from flask_restful import Resource
from api.resources.v1.users import User

''' This method handles user authentication and authorization ''' 

def authenticate(email, password):
    # Check if user is found in records
    user = User.get_user(email, password)
    return user

def identity(payload):
    user_email = payload['identity']
    return User.get_user(user_email, None)

def log_out():
    pass    