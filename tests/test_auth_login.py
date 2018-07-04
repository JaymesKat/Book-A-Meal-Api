import json
from tests.test_main import MainTest


class LoginTestCase(MainTest):
    ''' Tests for user login authentication '''

    '''Test if user logged in successfully'''

    def test_registered_user_log_in(self):
        test_data = {
            "first_name": "Joshua",
            "last_name": "Mugisha",
            "user_name": "jmugisha",
            "email": "joshua@example.com",
            "password": "@password"}
        res = self.client.post(
            '/api/v1/auth/register/',
            data=json.dumps(test_data))
        registered_data = json.loads(res.data.decode())
        self.assertTrue(
            registered_data['message'] == 'User {} was created'.format(
                test_data['user_name']))
        self.assertEqual(res.status_code, 201)

        res1 = self.client.post('/api/v1/auth/login/',
                                data=json.dumps({"email": "joshua@example.com",
                                                 "password": "@password"}),
                                content_type='application/json')
        data = json.loads(res1.data.decode())
        self.assertTrue(data['message'] == 'Successfully logged in')
        self.assertTrue(data['access_token'])
        self.assertTrue(res1.content_type == 'application/json')
        self.assertEqual(res1.status_code, 200)

    '''Test if a user attempted to login in with missing credentials'''

    def test_user_logging_in_with_missing_credentials(self):
        test_data = json.dumps({'username': '', 'email': '', 'password': ''})
        res = self.client.post(
            '/api/v1/auth/login/',
            data=test_data,
            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertIn('Bad Request', result['error'])
        self.assertEqual(res.status_code, 401)

    def test_unregistered_user_login(self):
        response = self.client.post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email='katarikawe@gmail.com',
                password='pass123'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['error'] == 'Bad Request')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 401)
