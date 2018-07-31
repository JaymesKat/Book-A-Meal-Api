import json
from tests.test_base_case import BaseTest


class RegistrationTestCase(BaseTest):
    ''' Tests for user registration '''
    def setUp(self):
        super(RegistrationTestCase, self).setUp()
        self.missing_data = json.dumps(
                        {
                            "first_name": "James",
                            "last_name": "",
                            "user_name": "",
                            "email": " ",
                            "password": " "
                        })


    def test_user_registered(self):
        '''Test if new user can be registered successfully'''
        res = self.client.post(
            '/api/v1/auth/register/',
            data=json.dumps(self.test_user),
            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            'User of email {} has been created'.format(
                self.test_user['email']),
            result['message'])

    def test_user_registered_missing_credentials(self):
        '''Test if a user registered with missing credentials'''

        res = self.client.post(
            '/api/v1/auth/register/',
            data=self.missing_data,
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertIn('No field should be empty', result['message'])

    def test_user_entered_invalid_email(self):
        '''Test if a user registered with invalid email'''
        test_data = json.dumps({"first_name": "James",
                                "last_name": "Katarikawe",
                                "user_name": "jpkat92",
                                "email": "nbdsfh2343",
                                "password": "pass",
                                "is_caterer": False})
        res = self.client.post(
            '/api/v1/auth/register/',
            data=test_data,
            content_type='application/json')
        result = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertIn(
            'This email is invalid.',
            result['Error'])

    def test_user_email_already_registered(self):
        ''' Test if user is already registered'''

        res = self.client.post(
            '/api/v1/auth/register/',
            data=json.dumps(self.test_user))
        res = self.client.post(
            '/api/v1/auth/register/',
            data=json.dumps(self.test_user))
        self.assertEqual(res.status_code, 409)
        result = json.loads(res.data.decode())
        self.assertIn("This email is already registered.", result['Error'])

    def test_user_name_already_registered(self):
        ''' Test if user is already registered'''
        test_data = json.dumps({"first_name": "Joshua",
                                "last_name": "Mugisha",
                                "user_name": "jmugisha",
                                "email": "joshua@example.com",
                                "password": "@123Joshuapassword",
                                "is_caterer": False})

        test_data_1 = json.dumps({"first_name": "Josh",
                                  "last_name": "Mug",
                                  "user_name": "jmugisha",
                                  "email": "joshua1@example.com",
                                  "password": "@123Joshuapassword",
                                  "is_caterer": False})
        res = self.client.post('/api/v1/auth/register/', data=test_data)
        res = self.client.post('/api/v1/auth/register/', data=test_data_1)
        self.assertEqual(res.status_code, 409)
        result = json.loads(res.data.decode())
        self.assertIn("This username is already taken.", result['Error'])
