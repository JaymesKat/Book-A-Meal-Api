from flask import  jsonify, request, abort, make_response
import jwt
from datetime import datetime, timedelta
from flask_restful import Resource

class User(Resource):

    users = [
        {
            'id': 1,
            'user_name': u'james_katarikawe',
            'email': u'jpkatarikawe@gmail.com',
            'password': u'james', 
            'is_caterer': False,
            'orders_sent' : []
        },
        {
            'id': 2,
            'user_name': u'paul_kayongo',
            'email': u'paulkayongo@gmail.com',
            'password': u'kayongo', 
            'is_caterer': False,
            'orders_sent' : []
        },
        {
            'id': 3,
            'user_name': u'joseph_odur',
            'email': u'odur@gmail.com',
            'password': u'odur', 
            'is_caterer': True,
            'orders_received' : []
        },
        {
            'email': u'seryazi@gmail.com',
            'user_name': u'phillip_seryazi',
            
            'password': u'seryazi', 
            'is_caterer': True,
            'orders_received' : []
        }
    ]

    def get(self, user_id):
        pass

    def put(self, todo_id):
        pass

    def register():
        request.get_json(force=True)
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        if not name or not email not password:
            response = jsonify({'error': 'None of the fields should be blank'})
            response.status_code = 400
            return response

        email_check = email_matches(email)
        username_check = username_matches(username)
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
            user_data = {
                'username': username,
                'email': email,
                'password': password,
                'is_caterer': False,

            }
            self.users.append(user_data)
            response = jsonify(
                {'Registration status': user_data.username + ' successfully registered!!'})
            response.status_code = 201
            return response
          

    def login():
        email = request.json['email']
        password = request.json['password']

        if not username and not password:
            response = jsonify({'error': 'Email and password field cannot be blank'})
            response.status_code = 400
            return response

        user_name_check = [username for user in self.users if user['password'] == password]
        if username in user_name_check:
            jwt_args = {"user_name": user_name, "exp": datetime.utcnow() + timedelta(minutes=60)}
            token = jwt.encode(jwt_args, app.config['SECRET_KEY'], algorithm='HS256')
            response = jsonify({'Message': 'You have logged in', 'Token': token.decode('utf-8')})
            return response
        else:
            response = jsonify({'Login error': 'Invalid credentials'})
            response.status_code = 401
            return response 

    def save(self,user):
        # Adds user to collection of users
        self.users.append(user)

    def username_matches(self, username):
        # check if username is present
        if any(user['username'] == username for user in self.users):
            return True
        return False

    def generate_token(self, user_id):
        # Generate an access token for user
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        # Decodes the access token from the Authorization header
        try:
            payload = jwt.decode(token, app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
    
     def password_matches(self, password):
        # check if password is correct
        if any(user['password'] == password for user in self.users):
            return True
        return False

    def email_matches(self, email):
        # check if email is present
        if any(user['email'] == email for user in self.users):
            return True
        return False