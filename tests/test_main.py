import unittest
import json
from app import app

class MainTest(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()

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

        