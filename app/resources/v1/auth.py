
import re
from marshmallow import fields
from app import ma
from flask import jsonify, request, redirect, abort
from flask_restful import Resource
from app.models import User


class UserSchema(ma.Schema):
    first_name = fields.String(required=True, dump_to='firstName')
    last_name = fields.String(required=True, dump_to='lastName')
    user_name = fields.String(required=True, dump_to='userName')
    email = fields.Email()
    password = fields.String(required=True)
    
    class Meta:
        fields = ('id', 'first_name', 'last_name')
    
    
class RegistrationResource(Resource):
    '''
        This class handles user registration
    '''

    def post(self):
        payload = request.get_json(force=True)
        check_missing_registration_fields(payload)

        user_name = request.json['user_name'].strip()
        email = request.json['email'].strip()
        password = request.json['password'].strip()
        first_name = request.json['first_name'].strip()
        last_name = request.json['last_name'].strip()
        is_caterer = request.json['is_caterer']

        if not User.email_is_valid(email):
            response = jsonify(
                {'Error': 'This email is invalid.'})
            response.status_code = 400
            return response

        # check for duplicate emails
        duplicate_email = User.query.filter_by(email=email).first()
        duplicate_username = User.query.filter_by(username=user_name).first()
        if duplicate_email:
            response = jsonify({'Error': 'This email is already registered.'})
            response.status_code = 409
            return response

        elif duplicate_username:
            response = jsonify({'Error': 'This username is already taken.'})
            response.status_code = 409
            return response
        elif is_weak_password(password):
            response = jsonify({
                'Error':
                'Enter a password that is more than 8 characters \
                long and includes at least 1 digit and uppercase letter.'
            })
            response.status_code = 400
            return response
        else:
            user = User(first_name=first_name,
                        last_name=last_name,
                        username=user_name,
                        email=email,
                        is_caterer=is_caterer)
            user.password = password
            user.save()
            response = jsonify(
                {'message': 'User of email {} has been created'.format(email)})
            response.status_code = 201
            return response


class LoginResource(Resource):
    ''' This method handles user authentication and authorization '''

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
        return redirect('/api/v1/auth/login/', code=307)


def is_weak_password(password):
    """
        Password should have at least 8 characters,
        1 upper case letter and 1 digit
    """
    too_short = len(password) < 8
    missing_digit = re.search(r"\d", password) is None
    missing_uppercase = re.search(r"[A-Z]", password) is None

    response = too_short or missing_digit or missing_uppercase
    return response


def check_missing_registration_fields(payload):
    reg_fields = ['first_name', 'last_name', 'user_name', 'email', 'password']
    for key in reg_fields:
            if key not in payload.keys():
                abort(
                    400,
                    description='Missing fields')
            elif not payload[key]:
                abort(400, description='No field should be empty')
