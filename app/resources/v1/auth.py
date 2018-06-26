import datetime
from flask import request, jsonify, redirect, url_for
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource
from app.resources.v1.users import UserResource

class RegistrationResource(Resource):
    ''' This class handles user registration '''    
    registration_fields = ['first_name', 'last_name', 'user_name', 'email','password']

    def post(self):
        request.get_json(force=True)

        for key in self.registration_fields:
            if key not in request.json.keys():
                response = jsonify({'Error': 'Missing fields: provide first name, last name, user name, email and password'})
                response.status_code = 400
                return response
            elif not request.json[key]:
                response = jsonify({'Error': 'No field should be empty'})
                response.status_code = 400
                return response

        
        user_name = request.json['user_name'].strip()
        email = request.json['email'].strip()
        password = request.json['password'].strip()
        first_name = request.json['first_name'].strip()
        last_name = request.json['last_name'].strip()

        if not UserResource.email_is_valid(email):
            response = jsonify({'Error': 'This email is invalid. Please check again and resend'})
            response.status_code = 400
            return response

        if UserResource.email_matches(email):
            response = jsonify({'Error': 'This email is already registered.'})
            response.status_code = 409
            return response

        elif UserResource.username_matches(user_name):
            response = jsonify({'Error': 'This username is already taken.'})
            response.status_code = 409
            return response
        else:
            UserResource.register(first_name, last_name,user_name,email,password)
            response = jsonify({'message': 'User {} was created'.format(user_name)})
            response.status_code = 201
            return response


class LoginResource(Resource):
    ''' This class handles user authentication and authorization ''' 
    @staticmethod
    def authenticate(email, password):
        user = UserResource.get_user(email, password)
        return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        return UserResource.get_user_by_id(user_id)

    def post(self):
        return redirect('/api/v1/auth/login/',code=307)
