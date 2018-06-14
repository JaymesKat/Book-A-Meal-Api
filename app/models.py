from   __init__ import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(60), unique=True, index=True, nullable=False)
    email = db.Column(db.String(60), unique=True, index=True, nullable=False)
    is_caterer = db.Column(db.Boolean,default=False)
    password = db.Column(db.String(30), nullable=False)
    orders = db.relationship('Order', backref='customer')

    def __init__(self, first_name, last_name,username, email, is_caterer, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.is_caterer = is_caterer
        self.password = password

    def __repr__(self):
        return '<Full Name: {} {}' .format(self.first_name, self.last_name)

menu_items = db.Table('menu_items',
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'), primary_key=True),
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True)
)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    price = db.Column(db.Float)
    orders = db.relationship('Order', backref='meal')

    def __repr__(self):
        return '<Meal: %r>' % self.name
    
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    items = db.relationship('Meal', secondary=menu_items, lazy='subquery',
        backref=db.backref('menus', lazy=True))

    def __repr__(self):
        return '<Menu created: %r>' % self.date_created

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    completed = db.Column(db.Boolean,default=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return '<Order: #%r>' % self.id
