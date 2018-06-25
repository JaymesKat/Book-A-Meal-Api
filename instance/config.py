import datetime
import os
# Multiple Configuration settings for app


class MainConfiguration(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'IbZM55FJyk'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login/'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=3600)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
    SQLALCHEMY_DATABASE_URI = ""


class ProductionEnvironment(MainConfiguration):
    DEBUG = False
    TESTING = False


class TestingEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True


class DevelopmentEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True


app_config = {
    'main_config': MainConfiguration,
    'production': ProductionEnvironment,
    'testing': TestingEnvironment,
    'development': DevelopmentEnvironment
}
