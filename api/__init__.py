from flask import Flask
from instance.config import app_config


'''Config options: main_config, production_env, testing_env, development_env'''

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
   
    return app

