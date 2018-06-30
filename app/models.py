import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class BaseModel(db.Model):
    '''
        This model defines a base for all models
    '''
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        

class User(BaseModel):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(60), unique=True, index=True, nullable=False)
    email = db.Column(db.String(60), unique=True, index=True, nullable=False)
    is_caterer = db.Column(db.Boolean,default=False)
    password_hash = db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order', backref='user')


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
    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'), primary_key=True)
)

class Meal(BaseModel):
    __tablename__ = "meals"
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
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    items = db.relationship('Meal', secondary=menu_items, lazy='subquery',
        backref=db.backref('menu', lazy=True))

    def __repr__(self):
        return '<Menu created: %r>' % self.items

class Order(BaseModel):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key = True)
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    completed = db.Column(db.Boolean,default=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)

    def __repr__(self):
        return '<Order: %r on %r>'%format(self.meal.name,self.date_submitted)