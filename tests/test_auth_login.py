import json
from tests.test_base_case import BaseTest


class LoginTestCase(BaseTest):
    ''' Tests for user login authentication '''
    def setUp(self):
        super(LoginTestCase, self).setUp()
        self.client.post(
            '/api/v1/auth/register/',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )

    def test_registered_user_log_in(self):
        '''Test if user logged in successfully'''

        res = self.client.post('/api/v1/auth/login/',
                               data=json.dumps({
                                "email": self.test_user["email"],
                                "password": self.test_user["password"]}),
                               content_type='application/json')
        data = json.loads(res.data.decode())
        self.assertTrue(data['message'] == 'Successfully logged in')
        self.assertTrue(data['token'])
        self.assertEqual(res.status_code, 200)

    def test_user_logging_in_with_missing_credentials(self):
        '''Test if a user attempted to login in with missing credentials'''

        test_data = json.dumps({'username': '', 'email': '', 'password': ''})
        res = self.client.post(
            '/api/v1/auth/login/',
            data=test_data,
            content_type='application/json')
        result = json.loads(res.data.decode())
        self.assertIn('Bad Request', result['error'])
        self.assertEqual(res.status_code, 401)

    def test_unregistered_user_cannot_login(self):
        '''Test if unregistered user cannot login'''

        response = self.client.post(
            '/api/v1/auth/login/',
            data=json.dumps({
                "email": 'katarikawe@gmail.com',
                "password": 'pass123'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['error'] == 'Bad Request')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 401)

    def test_redirect_on_no_trailing_slash(self):

        res_1 = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                            "email": "joshua@example.com",
                            "password": "@123Joshuapassword"
                            }),
            content_type='application/json')

        # check that the redirect happened
        self.assertEqual(res_1.status_code, 307)


if __name__ == "__main__":
    super.unittest.main()
