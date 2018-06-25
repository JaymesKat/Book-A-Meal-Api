import unittest
import json
from app.__init__ import app
from app import create_app, db


class BaseTest(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
         

        self.customer = json.dumps({
            'email': 'paulkayongo@gmail.com',
            'password': 'kayongo'
        })

        self.caterer = json.dumps({
            "email": "odur@gmail.com",
            "password": "odur"
        })

        self.order = json.dumps({
            'meal_id': 5
        })

        self.meal = json.dumps({
            "name": "Posho & Meat",
            "price": "10.5"
        })

        self.menu_list = json.dumps({
            'meal_ids': [4, 2]
        })

    
    def tearDown(self): 
        db.session.remove() 
        db.drop_all() 
        self.app_context.pop()