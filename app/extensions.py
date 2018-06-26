from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required
from flask_marshmallow import Marshmallow
from resources.v1.auth import LoginResource

jwt = JWT(authentication_handler=LoginResource.authenticate, identity_handler=LoginResource.identity)

# Define response fields for successful login
@jwt.auth_response_handler
def auth_response_handler(access_token, identity):
    return jsonify({
            "message": "Successfully logged in",
            'email': identity.email,
            'access_token': access_token.decode('utf-8'),
            'user_id': identity.id,
            'is_admin': identity.is_caterer
        })

# Initialize SQLAlchemy ORM instance
db = SQLAlchemy()

# Initialize Marshmallow package for object serialization/deserialization
ma = Marshmallow()

