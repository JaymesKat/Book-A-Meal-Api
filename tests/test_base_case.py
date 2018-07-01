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
        })

        customer_info = json.dumps({
            "first_name": "Paul",
            "last_name": "Kayongo",
            "user_name": "kayongo",
            "email": "paulkayongo@gmail.com",
            "password": "kayongo",
            "is_caterer": False
        })

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

        # Add meals for creating menu
        res = self.client.post(
            '/api/v1/auth/login/',
            data=self.caterer,
            content_type='application/json')
        res_data = json.loads(res.data.decode())

        res_1 = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(
                {
                    "name": "Pilau",
                    "price": "12"}),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['access_token']))

        response_data = json.loads(res_1.data.decode())
        meal_id_1 = int(response_data['Meal'][0]['id'])

        res_2 = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(
                {
                    "name": "Fish Tikka",
                    "price": "14"}),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['access_token']))

        response_data = json.loads(res_2.data.decode())
        meal_id_2 = int(response_data['Meal'][0]['id'])

        res_3 = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(
                {
                    "name": "Chicken Tikka",
                    "price": "17"}),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['access_token']))

        response_data = json.loads(res_3.data.decode())
        meal_id_3 = int(response_data['Meal'][0]['id'])

        res_4 = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(
                {
                    "name": "Chicken Curry",
                    "price": "14"}),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['access_token']))

        response_data = json.loads(res_4.data.decode())
        meal_id_4 = int(response_data['Meal'][0]['id'])

        # Add items to the menu
        self.menu_list = json.dumps(
            {"meal_ids": [meal_id_1, meal_id_2, meal_id_3, meal_id_4]})

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
