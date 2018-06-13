from   __init__ import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(30), unique=True, index=True, nullable=False)
    is_caterer = db.Column(db.Boolean,default=False)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return '<First Name: {} and Last Name: {}' .format(self.first_name, self.last_name)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    price = db.Column(db.Float)

    def __repr__(self):
        return '<Meal: %r>' % self.name
    
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Menu created: %r>' % self.date_created

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'),nullable=False)
    menu = db.relationship('Menu', backref=db.backref('menus'))

    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'),nullable=False)
    meal = db.relationship('Meal', backref=db.backref('meals'))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    completed = db.Column(db.Boolean,default=False)

    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'),nullable=False)
    meal = db.relationship('Meal', backref=db.backref('meals'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User', backref=db.backref('users'))

    def __repr__(self):
        return '<Order: #%r>' % self.id
    