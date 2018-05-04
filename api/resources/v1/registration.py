from flask import jsonify, request
from flask_restful import Resource
from api.resources.v1.users import User

''' This class handles user registration '''
class Registration(Resource):
   
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

        if not User.email_is_valid(email):
            response = jsonify({'Error': 'This email is invalid. Please check again and resend'})
            response.status_code = 400
            return response

        if User.email_matches(email):
            response = jsonify({'Error': 'This email is already registered.'})
            response.status_code = 409
            return response

        elif User.username_matches(user_name):
            response = jsonify({'Error': 'This username is already taken.'})
            response.status_code = 409
            return response
        else:
            User.register(first_name, last_name,user_name,email,password)
            response = jsonify({'message': 'User {} was created'.format(user_name)})
            response.status_code = 201
            return response
