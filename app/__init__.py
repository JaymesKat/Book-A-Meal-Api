from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from flask_restful import Api
from instance.config import app_config
from .extensions import db, ma
from flask_jwt import JWT
from .resources.v1.meals import MealResource, MealListResource
from .resources.v1.orders import OrderResource, OrderListResource
from .resources.v1.menu import MenuResource, MenuSingleResource
from .resources.v1.auth import RegistrationResource, LoginResource


jwt = JWT(authentication_handler=LoginResource.authenticate,
          identity_handler=LoginResource.identity)


@jwt.auth_response_handler
def auth_response_handler(token, identity):
    # Define response fields for successful login
    resp = jsonify({
        "message": "Successfully logged in",
        'email': identity.email,
        'token': token.decode('utf-8'),
        'userId': identity.id,
        'isAdmin': identity.is_caterer,
        'firstName': identity.first_name
    })
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get(
            'Access-Control-Request-Headers', 'Authorization')
    return resp


class ApiInstance(object):

    def __init__(self, api_instance):
        self.api = api_instance

    def setup_routes(self):

        self.api.add_resource(
            RegistrationResource,
            '/api/v1/auth/register/',
            '/api/v1/auth/register',
            endpoint="register",
            strict_slashes=False)

        self.api.add_resource(
            LoginResource,
            '/api/v1/auth/login',
            endpoint="jwt")

        self.api.add_resource(
            OrderListResource,
            '/api/v1/orders/',
            '/api/v1/orders',
            endpoint="order",
            strict_slashes=False)

        self.api.add_resource(
            OrderResource,
            '/api/v1/orders/<int:order_id>',
            '/api/v1/orders/<int:order_id>/')

        self.api.add_resource(
            MealListResource,
            '/api/v1/meals/',
            '/api/v1/meals',
            endpoint="meal",
            strict_slashes=False)

        self.api.add_resource(
            MealResource,
            '/api/v1/meals/<int:meal_id>',
            '/api/v1/meals/<int:meal_id>/')

        self.api.add_resource(
            MenuResource,
            '/api/v1/menu/',
            '/api/v1/menu',
            endpoint="menu",
            strict_slashes=False)
        
        self.api.add_resource(
            MenuSingleResource,
            '/api/v1/menu/<int:day_id>',
            '/api/v1/menu/<int:day_id>',
            strict_slashes=False)


def configure_extensions(app):
    """configure flask extensions
    """
    jwt.init_app(app)
    db.init_app(app)
    ma.init_app(app)


def create_app(config_name):
    """
        Function definition for creating application instance
    """
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    from .main import default as default_bp
    app.register_blueprint(default_bp)

    # Define blueprint for api
    api_bp = Blueprint('api', __name__, template_folder='templates')
    api = Api(api_bp)

    # Setup api endpoints
    api_instance = ApiInstance(api)
    api_instance.setup_routes()
    # Register api blueprint
    app.register_blueprint(api_bp)

    configure_extensions(app)
    
    CORS(app,
         resources={r"/api/*": {"origins": "*"}},
         allow_headers=["Content-Type",
                        "Authorization",
                        "Access-Control-Allow-Credentials"],
         supports_credentials=True)

    # Push application context
    app.app_context().push()

    @app.after_request
    def add_cors(resp):
        """
        Ensure all responses have the CORS headers.
        This ensures any failures are also accessible by the client.
        """
        resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE'
        resp.headers['Access-Control-Allow-Headers'] = request.headers.get(
            'Access-Control-Request-Headers', 'Authorization')
        return resp

    return app


# Create flask app instance
app = create_app('development')
