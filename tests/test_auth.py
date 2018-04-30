import unittest
import json
from api.app import app


# Tests for user authentication
class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        
        # set app to testing mode
        self.app.testing = True

        # initialize test client
        self.client = self.app.test_client

        
     # Test if new user can be registered successfully
    def test_user_registered(self):
        test_data = json.dumps(
            {
            'email': 'james@example.com',
            'password': '@password'
            })

        res = self.client().post('/bookameal/api/v1/auth/register', data=test_data)
        # assert that the request contains a 201 status code
        self.assertEqual(res.status_code, 201)

    def test_user_already_registered(self):
        # Test that a user is already registered
        test_data = json.dumps(
            {
            'email': 'james@example.com',
            'password': '@password'
            })
        res = self.client().post('/bookameal/api/v1/', data=test_data)
        res = self.client().post('/bookameal/api/v1/', data=test_data)
        self.assertEqual(res.status_code, 409)
        second_res = self.client().post('/bookameal/api/v1/auth/register', data=self.user)

        # Status code returned should be 201 indicating that data received by server 
        # is correct but is server has not processed it since it is duplicate
        self.assertEqual(second_res.status_code, 202)
        # get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User already exists. Please use another email.")
