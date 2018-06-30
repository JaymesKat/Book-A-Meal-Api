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

        caterer_info = json.dumps({
            "first_name": "Joseph",
            "last_name": "Odur",
            "user_name": "odur",
            "email": "odur@gmail.com",
            "password": "odur",
            "is_caterer": True
        }
        )

        customer_info = json.dumps({
            "first_name": "Paul",
            "last_name": "Kayongo",
            "user_name": "kayongo",
            "email": "paulkayongo@gmail.com",
            "password": "kayongo",
            "is_caterer": False
        }
        )

        self.client.post('/api/v1/auth/register/',
                         data=caterer_info,
                         content_type='application/json')

        self.client.post('/api/v1/auth/register/',
                         data=customer_info,
                         content_type='application/json')

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
