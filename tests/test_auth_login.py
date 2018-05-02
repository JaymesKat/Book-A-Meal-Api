import unittest
import json
from api.app import app

class LoginTestCase(unittest.TestCase):   
    ''' Tests for user login authentication '''
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client

    '''Test if new user can be registered successfully'''
    def test_user_registered(self):
        test_data = json.dumps(
            {'email': 'james@example.com', 'password': '@password'})

        res = self.client().post('/bookameal/api/v1/auth/register', data=test_data)
        self.assertEqual(res.status_code, 201)

    '''Test if a user registered with missing credentials'''
    def test_user_registered_missing_credentials(self):
        test_data = json.dumps({'username': '','email': '', 'password': ''}) 
        res = self.client().post('/bookameal/api/v1/auth/register', data=test_data) 

    ''' Test if user is already registered'''
    def test_user_already_registered(self):
        test_data = json.dumps(
            {'email': 'james@example.com', 'password': '@password'})
        res = self.client().post('/bookameal/api/v1/auth/register/', data=test_data)
        res = self.client().post('/bookameal/api/v1/auth/register/', data=test_data)
        self.assertEqual(res.status_code, 409)
        second_res = self.client().post('/bookameal/api/v1/auth/register', data=test_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User already exists. Please use another email")
