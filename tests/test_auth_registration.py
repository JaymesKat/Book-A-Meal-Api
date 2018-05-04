import unittest
import json
from api.app import app

class RegistrationTestCase(unittest.TestCase):   
    ''' Tests for user registration '''

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client

    def test_user_registered(self):
        '''Test if new user can be registered successfully'''
        test_data = {"first_name": "Winnie", "last_name": "Mandela", "user_name": "mandela", "email": "mandela@example.com", "password": "@password123"}

        res = self.client().post('/api/v1/auth/register/', data=json.dumps(test_data),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode())
        self.assertIn('User {} was created'.format(test_data['user_name']), result['message'])

    def test_user_registered_missing_credentials(self):
        '''Test if a user registered with missing credentials'''
        test_data = json.dumps({"first_name": "James", "last_name": "", "user_name": "", "email": " ", "password": " "})
        res = self.client().post('/api/v1/auth/register/', data=test_data,content_type='application/json')
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertIn('No field should be empty',result['Error'])

    def test_user_already_registered(self):
        ''' Test if user is already registered'''
        test_data = json.dumps({"first_name": "James", "last_name": "Katarikawe", "user_name": "jameskatarikawe", "email": "james@example.com", "password": "@password"})
        res = self.client().post('/api/v1/auth/register/', data=test_data)
        res = self.client().post('/api/v1/auth/register/', data=test_data)
        self.assertEqual(res.status_code, 409)
        result = json.loads(res.data.decode())
        self.assertIn("This email is already registered.", result['Error'])
