from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from instance.config import app_config
from api.resources.v1.users import User
from api.resources.v1.login import authenticate, identity

jwt = JWT(authentication_handler=authenticate, identity_handler=identity)
'''Config options: main_config, production_env, testing_env, development_env'''

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    jwt.init_app(app)
    return app

