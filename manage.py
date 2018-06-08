import unittest
from flask_script import Manager
from app.app import app

manager = Manager(app)

''' Define command to run all tests '''


@manager.command
def test():
    # Run unit tests
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=1).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
