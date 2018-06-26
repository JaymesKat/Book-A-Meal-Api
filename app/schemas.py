from . import app, ma
from .models import Meal, Menu, Order, User

class MealSchema(ma.Schema):
    class Meta:
        model = Meal

class MenuSchema(ma.Schema):
    class Meta:
        model = Menu

class OrderSchema(ma.Schema):
    class Meta:
        model = Order

class UserSchema(ma.Schema):
    class Meta:
        model = User