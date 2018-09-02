# flake8: noqa
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy_utils import database_exists, create_database, drop_database
from app import app, db
from db_setup import insert_table_data

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

''' Define command to run all tests '''


@manager.command
def test():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


''' Define command to create database'''


@manager.command
def resetdb():
    """Destroys and creates the database + tables."""
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    if database_exists(db_url):
        print('Deleting database.')
        drop_database(db_url)
    if not database_exists(db_url):
        print('Creating database.')
        create_database(db_url)

    print('Creating tables.')

    from app.models import User, Meal, Menu, Order, Day
    db.create_all()
    insert_table_data(db)
    print('Book-A-Meal tables created with data!')


if __name__ == "__main__":
    manager.run()
