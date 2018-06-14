import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy_utils import database_exists, create_database, drop_database
from app.__init__ import app, db

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
    from app.models import User, Meal, Menu, Order
    db.create_all()

    customer1 = User(first_name='James',last_name='Katarikawe',username='james_katarikawe', email='james@example.com',is_caterer=False,password='james')
    customer2 = User(first_name='Paul',last_name='Kayongo',username='paul_kayongo', email='paulkayongo@gmail.com',is_caterer=False,password='kayongo')
    admin1 = User(first_name='Joseph',last_name='Odur',username='joseph_odur', email='odur@gmail.com',is_caterer=True,password='odur')
    admin2 = User(first_name='Phillip',last_name='Seryazi',username='phillip_seryazi', email='seryazi@gmail.com',is_caterer=True,password='odur')
    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(admin1)
    db.session.add(admin2)


    meal1 = Meal(name="Rice & Chicken", price=10.5)
    meal2 = Meal(name="Posho & Beans", price=9.0)
    meal3 = Meal(name="Potatoes & Meat", price=12)
    meal4 = Meal(name="Spaghetti", price=11)
    db.session.add(meal1)
    db.session.add(meal2)
    db.session.add(meal3)

    menu = Menu()

    menu.items.append(meal1)
    menu.items.append(meal2)
    menu.items.append(meal3)
    menu.items.append(meal4)
    db.session.add(menu)

    order1 = Order(meal=meal1,customer=customer1)
    order2 = Order(meal=meal3,customer=customer2)
    db.session.add(order1)
    db.session.add(order2)

    db.session.commit()

    print('Book-A-Meal tables created with data!')

if __name__ == "__main__":
    manager.run()

