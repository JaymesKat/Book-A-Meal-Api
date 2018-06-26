import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import app, db

class BaseModel(db.Model):
    '''
        This model defines a base for all models
    '''
    __abstract__ = True

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        

class User(BaseModel):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(60), unique=True, index=True, nullable=False)
    email = db.Column(db.String(60), unique=True, index=True, nullable=False)
    is_caterer = db.Column(db.Boolean,default=False)
    password = db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order', backref='user')

    def __init__(self, first_name, last_name,username, email, is_caterer):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.is_caterer = is_caterer

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

menu_items = db.Table('menu_items',
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'), primary_key=True),
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True)
)

class Meal(BaseModel):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    price = db.Column(db.Float)
    orders = db.relationship('Order', backref='meal')

    def __repr__(self):
        return '<Meal: %r>' % self.name

    def __init__(self, name, price):
        self.name = name
        self.price = price
    
class Menu(BaseModel):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    items = db.relationship('Meal', secondary=menu_items, lazy='subquery',
        backref=db.backref('menu', lazy=True))

    def __repr__(self):
        return '<Menu created: %r>' % self.date_created

class Order(BaseModel):
    id = db.Column(db.Integer, primary_key = True)
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    completed = db.Column(db.Boolean,default=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return '<Order: %r on %r>',format(self.meal.name,self.date_submitted)