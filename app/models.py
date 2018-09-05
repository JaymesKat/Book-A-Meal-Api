import datetime
import calendar
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email import validate_email
from . import db

my_date = datetime.datetime.today()


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
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(
        db.String(60),
        unique=True,
        index=True,
        nullable=False)
    email = db.Column(db.String(60), unique=True, index=True, nullable=False)
    is_caterer = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128), nullable=False)
    orders_received = db.relationship(
        'Order',
        foreign_keys='Order.caterer_id',
        cascade='all, delete-orphan')
    orders = db.relationship(
        'Order',
        foreign_keys='Order.user_id',
        cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def email_is_valid(email):
        is_valid = validate_email(email)
        return is_valid


menu_items = db.Table(
    'menu_items',
    db.Column(
        'menu_id',
        db.Integer,
        db.ForeignKey('menu.id'),
        primary_key=True),
    db.Column(
        'meal_id',
        db.Integer,
        db.ForeignKey('meals.id'),
        primary_key=True))


class Meal(BaseModel):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    price = db.Column(db.Float)
    caterer_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                         nullable=True)
    orders = db.relationship(
        'Order',
        backref='meal',
        cascade='all, delete-orphan')
    caterer = db.relationship('User',
                              foreign_keys=[caterer_id])

    def __repr__(self):
        return '<Meal {}: {}>'.format(self.id, self.name)



class Day(BaseModel):
    __tablename__ = 'days'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,
                     default=calendar.day_name[my_date.weekday()],
                     nullable=False)


class Menu(BaseModel):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    caterer_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                         nullable=True)
    day_id = db.Column(db.Integer, db.ForeignKey('days.id'),
                       default=my_date.weekday()+1,
                       nullable=True)
    items = db.relationship('Meal', secondary=menu_items, lazy='subquery',
                            backref=db.backref('menu', lazy=True))
    caterer = db.relationship('User',
                              foreign_keys=[caterer_id])


class Order(BaseModel):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    caterer_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                           nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer = db.relationship('User',
                               foreign_keys=[user_id])
    caterer = db.relationship('User',
                              foreign_keys=[caterer_id])

    def __repr__(self):
        return '<Order {}: Meal id:{} by User id:{} at {}>' % format(
            self.id, self.meal_id, self.user_id, self.date_submitted)
