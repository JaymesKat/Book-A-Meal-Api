import os
from flask import Flask, jsonify, Blueprint
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from instance.config import app_config
from .resources.v1.auth import LoginResource

jwt = JWT(authentication_handler=LoginResource.authenticate,
          identity_handler=LoginResource.identity)

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

# Function definition for creating application instance


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    # Push application context
    app.app_context().push()

    from .main import default as default_bp
    app.register_blueprint(default_bp)

    # Define blueprint for api
    api_bp = Blueprint('api', __name__, template_folder='templates')
    api = Api(api_bp)

    # Setup api endpoints
    from .app import ApiInstance
    api_instance = ApiInstance(api)
    api_instance.setup_routes()
    # Register api blueprint
    app.register_blueprint(api_bp)

    jwt.init_app(app)

    return app


# Create flask app instance
app = create_app('development')
