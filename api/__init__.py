from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from instance.config import app_config
from api.app import setup_routes
from api.resources.v1.users import User
from api.resources.v1.login import Login

jwt = JWT(authentication_handler=Login.authenticate, identity_handler=Login.identity)
'''Config options: main_config, production_env, testing_env, development_env'''

@jwt.auth_response_handler
def auth_response_handler(access_token, identity):
    return jsonify({
            "message": "Successfully logged in",
            'email': identity.email,
            'access_token': access_token.decode('utf-8'),
            'user_id': identity.id
        })

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    jwt.init_app(app)
    return app

app = create_app('development_env')

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
setup_routes(api)
app.register_blueprint(api_bp)
