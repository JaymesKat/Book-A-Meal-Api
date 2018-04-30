# Multiple Configuration settings for app

class MainConfiguration(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True

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