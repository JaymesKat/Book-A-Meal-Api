import unittest
import json
from app.__init__ import app
from app import create_app, db
from app.models import Day


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        day1 = Day(name="Monday")
        db.session.add(day1)
        db.session.commit()

        caterer_info = json.dumps({
            "first_name": "Joseph",
            "last_name": "Odur",
            "user_name": "odur",
            "email": "odur@gmail.com",
            "password": "123OdurJoseph",
            "is_caterer": True
        })

        customer_info = json.dumps({
            "first_name": "Paul",
            "last_name": "Kayongo",
            "user_name": "kayongo",
            "email": "paulkayongo@gmail.com",
            "password": "@123Paulkayongo",
            "is_caterer": False
        })

        self.test_user = {
            "first_name": "Winnie",
            "last_name": "Mandela",
            "user_name": "mandela",
            "email": "mandela@example.com",
            "password": "@Password123",
            "is_caterer": False}

        res = self.client.post('/api/v1/auth/register/',
                               data=caterer_info,
                               content_type='application/json')     
        self.client.post('/api/v1/auth/register/',
                         data=customer_info,
                         content_type='application/json')

        self.customer = json.dumps({
            'email': 'paulkayongo@gmail.com',
            'password': '@123Paulkayongo'
        })

        self.caterer = json.dumps({
            "email": "odur@gmail.com",
            "password": "123OdurJoseph"
        })

        self.meal = json.dumps({
            "name": "Posho & Meat",
            "price": "10.5"
        })

        # Login a caterer and customer
        res = self.client.post(
            '/api/v1/auth/login/',
            data=self.caterer,
            content_type='application/json')
        res_data = json.loads(res.data.decode())
        self.caterer_token = res_data['token']
        self.caterer_id = res_data['userId']

        res1 = self.client.post(
            '/api/v1/auth/login/',
            data=self.customer,
            content_type='application/json')
        res_data = json.loads(res1.data.decode())
        self.customer_token = res_data['token']
        
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
                    "name": "Pasta",
                    "price": "12"}),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['token']))

        response_data = json.loads(res_1.data.decode())
        meal_id_1 = response_data['Meal']['id']

        res_2 = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(
                {
                    "name": "Fish Tikka",
                    "price": "14"}),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['token']))

        response_data = json.loads(res_2.data.decode())
        meal_id_2 = int(response_data['Meal']['id'])

        res_3 = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(
                {
                    "name": "Chicken Tikka",
                    "price": "17"}),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['token']))

        response_data = json.loads(res_3.data.decode())
        meal_id_3 = int(response_data['Meal']['id'])

        res_4 = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(
                {
                    "name": "Chicken Curry",
                    "price": "14"}),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['token']))

        response_data = json.loads(res_4.data.decode())
        meal_id_4 = int(response_data['Meal']['id'])

        # Add items to the menu
        self.menu_list = json.dumps(
            {
                "day": 1,
                "meal_ids": [meal_id_1, meal_id_2, meal_id_3, meal_id_4]
            })

        self.order = json.dumps({
            'caterer_id': self.caterer_id,
            'meal_id': meal_id_1
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
