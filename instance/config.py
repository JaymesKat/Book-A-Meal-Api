import datetime
import os

POSTGRES_URL = os.environ.get("POSTGRES_URL")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PW = os.environ.get("POSTGRES_PW")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

# Multiple Configuration settings for app

class MainConfiguration(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'IbZM55FJyk'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login/'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=3600)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  


class ProductionEnvironment(MainConfiguration):
    DEBUG = False
    TESTING = False


class TestingEnvironment(MainConfiguration):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(MainConfiguration.BASE_DIR, 'data-test.sqlite')
    DEBUG = True
    TESTING = True


class DevelopmentEnvironment(MainConfiguration):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(POSTGRES_USER,POSTGRES_PW,POSTGRES_URL,POSTGRES_DB)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = True
    TESTING = True


app_config = {
    'main_config': MainConfiguration,
    'production_env': ProductionEnvironment,
    'testing_env': TestingEnvironment,
    'development_env': DevelopmentEnvironment
}
