import unittest
import json
from api.app import app

class LoginTestCase(unittest.TestCase):   
    ''' Tests for user login authentication '''
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client

    '''Test if user logged in successfully'''
    def test_user_logged_in(self):
        test_data = {'email': 'james@example.com', 'password': '@password'}

        res = self.client().post('/bookameal/api/v1/auth/login', data=json.dumps(test_data))
        self.assertEqual(res.status_code, 201)

    '''Test if a user attempted to login in with missing credentials'''
    def test_user_logging_in_with_missing_credentials(self):
        test_data = json.dumps({'username': '','email': '', 'password': ''}) 
        res = self.client().post('/bookameal/api/v1/auth/login', data=test_data) 
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertIn('No field should be empty',result['Error'])

    ''' Test if user is already logged in'''
    def test_user_already_logged_in(self):
        test_data = json.dumps(
            {'email': 'james@example.com', 'password': '@password'})
        res = self.client().post('/bookameal/api/v1/auth/login/', data=test_data)
        res = self.client().post('/bookameal/api/v1/auth/login/', data=test_data)
        self.assertEqual(res.status_code, 409)
        second_res = self.client().post('/bookameal/api/v1/auth/login', data=test_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User already logged in")
