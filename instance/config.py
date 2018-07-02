import datetime
import os
from dotenv import load_dotenv

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

POSTGRES_URL = os.environ.get("POSTGRES_URL") or "localhost"
POSTGRES_USER = os.environ.get("POSTGRES_USER") or "jameskatarikawe"
POSTGRES_PW = os.environ.get("POSTGRES_PW") or ""
POSTGRES_DB = os.environ.get("POSTGRES_DB") or "book_a_meal"
POSTGRES_TEST_DB = os.environ.get("POSTGRES_TEST_DB")  or "book_a_meal_test"

# Multiple Configuration settings for app

class MainConfiguration(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'IbZM55FJyk'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login/'
    JWT_AUTH_USERNAME_KEY = os.environ.get('JWT_AUTH_USERNAME_KEY') or 'email'
    JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=3600)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  


class ProductionEnvironment(MainConfiguration):
    DEBUG = False
    TESTING = False


class TestingEnvironment(MainConfiguration):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format("postgres","",POSTGRES_URL,POSTGRES_TEST_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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
    'production': ProductionEnvironment,
    'testing': TestingEnvironment,
    'development': DevelopmentEnvironment
}
