from flask import Flask, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from instance.config import app_config
from api.resources.v1.users import User
from api.resources.v1.login import Login

jwt = JWT(authentication_handler=Login.authenticate, identity_handler=Login.identity)
'''Config options: main_config, production_env, testing_env, development_env'''

@jwt.auth_response_handler
def auth_response_handler(access_token, identity):
    return jsonify({
            'access_token': access_token.decode('utf-8'),
            'user_email': identity.email,
            'user_name': identity.first_name+" "+identity.last_name,
            "message": "Successfully logged in"
        })

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    jwt.init_app(app)
    return app

