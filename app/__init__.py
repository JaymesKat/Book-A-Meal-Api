from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required
from instance.config import app_config
from app import ApiInstance
from resources.v1.login import LoginResource

jwt = JWT(authentication_handler=LoginResource.authenticate, identity_handler=LoginResource.identity)
'''Config options: main_config, production_env, testing_env, development_env'''

@jwt.auth_response_handler
def auth_response_handler(access_token, identity):
    return jsonify({
            "message": "Successfully logged in",
            'email': identity.email,
            'access_token': access_token.decode('utf-8'),
            'user_id': identity.id,
            'is_admin': identity.is_caterer
        })

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    jwt.init_app(app)
    return app

app = create_app('development_env')

db = SQLAlchemy(app)

api_bp = Blueprint('api', __name__, template_folder='templates')
api = Api(api_bp)

#Setup routes
api_instance = ApiInstance(api)
api_instance.setup_routes()

app.register_blueprint(api_bp)
