
import pdb 
from flask import jsonify, request, redirect
from flask_restful import Resource
from app.models import User

''' This class handles user registration '''
class RegistrationResource(Resource):
   
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
        is_caterer = request.json['is_caterer']

        if not User.email_is_valid(email):
            response = jsonify({'Error': 'This email is invalid. Please check again and resend'})
            response.status_code = 400
            return response

        # check for duplicate emails
        duplicate_email = User.query.filter_by(email=email).first()
        duplicate_username = User.query.filter_by(username=user_name).first()
        if duplicate_email:
            response = jsonify({'Error':'This email is already registered.'})
            response.status_code = 409
            return response

        elif duplicate_username:
            response = jsonify({'Error': 'This username is already taken.'})
            response.status_code = 409
            return response

        else:
            user = User(first_name=first_name,
                        last_name=last_name,
                        username=user_name, 
                        email=email,
                        is_caterer=is_caterer)
            user.password = password
            user.save()
            response = jsonify({'message': 'User of email {} has been created'.format(email)})
            response.status_code = 201
            return response

''' This method handles user authentication and authorization ''' 
class LoginResource(Resource):

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            return user

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        user = User.query.get(user_id)
        return user

    def post(self):
        return redirect('/api/v1/auth/login/',code=307)