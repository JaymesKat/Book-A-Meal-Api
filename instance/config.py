import datetime
# Multiple Configuration settings for app


class MainConfiguration(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'IbZM55FJyk'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login/'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=3600)


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
    'production_env': ProductionEnvironment,
    'testing_env': TestingEnvironment,
    'development_env': DevelopmentEnvironment
}
