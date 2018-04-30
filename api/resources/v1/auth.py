 from flask import  jsonify, request, abort, make_response
from flask_restful import Resource
from api.resources.v1.users import User

class Authentication(Resource):
 
 
    def register():
        
        # Store posted user data in variables
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        if not name or not email not password:
            response = jsonify({'error': 'Missing fields'})
            response.status_code = 400
            return response

        email_check = User.email_matches(email)
        username_check = User.username_matches(username)
        if email in email_check:
            response = jsonify({'Error': 'This email is already registered.'})
            response.status_code = 409
            return response
        elif:
            if username in username_check:
            response = jsonify({'Error': 'This username is already taken.'})
            response.status_code = 409
            return response
        else:
            # All user data is present and unique
            user_data = {
                'username': username,
                'email': email,
                'password': password
            }
            self.users.append(user_data)
            response = jsonify(
                {'Message': user_data.username + ' successfully registered!!'})
            response.status_code = 201
            return response
          
    def login():
        email = request.json['email']
        password = request.json['password']

        if not username and not password:
            response = jsonify({'error': 'Email or/and password field cannot be blank'})
            response.status_code = 400
            return response

        username_check = User.email_matches(email)
        if username in user_name_check:
            jwt_args = {"user_name": user_name, "exp": datetime.utcnow() + timedelta(minutes=60)}
            token = jwt.encode(jwt_args, app.config['SECRET_KEY'], algorithm='HS256')
            response = jsonify({'Message': 'You have logged in', 'Token': token.decode('utf-8')})
            return response
        else:
            response = jsonify({'Login error': 'Invalid credentials'})
            response.status_code = 401
            return response 

 