import json
from tests.test_base_case import BaseTest

"""This class contains unit tests for the menu apis and functions"""


class MenuTestCase(BaseTest):

    def test_api_caterer_can_setup_menu(self):
        """ Test API can create a menu """
        res = self.client.post(
            '/api/v1/auth/login/',
            data=self.caterer,
            content_type='application/json')

        res_data = json.loads(res.data.decode())
        self.assertTrue(res_data['message'] == 'Successfully logged in')
        self.assertTrue(res_data['access_token'])

        res = self.client.post(
            '/api/v1/menu/',
            data=self.menu_list,
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['access_token']))

        self.assertEqual(res.status_code, 201)
        menu = json.loads(res.data.decode())

        meal_ids = json.loads(self.menu_list)["meal_ids"]

        # Check if meal ids on created menu match with posted ids
        self.assertEquals(meal_ids, menu["meal_ids"])

    def test_api_customer_should_not_setup_menu(self):
        """ Test API endpoint can create a meal option """

        res = self.client.post(
            '/api/v1/auth/login/',
            data=self.customer,
            content_type='application/json')
        res_data = json.loads(res.data.decode())
        self.assertTrue(res_data['message'] == 'Successfully logged in')
        self.assertTrue(res_data['access_token'])

        res = self.client.post(
            '/api/v1/menu/',
            data=self.menu_list,
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['access_token']))

        self.assertEqual(res.status_code, 403)
        self.assertIn(
            'You must be an admin to access this resource', str(
                res.data))

    def test_api_get_menu(self):
        # Test API can get menu with GET request
        res = self.client.post(
            '/api/v1/auth/login/',
            data=self.caterer,
            content_type='application/json')
        res_data = json.loads(res.data.decode())

        self.assertTrue(res_data['message'] == 'Successfully logged in')
        self.assertTrue(res_data['access_token'])

        self.client.post(
            '/api/v1/menu/',
            data=self.menu_list,
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['access_token']))

        res = self.client.get(
            '/api/v1/menu/',
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                res_data['access_token']))
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    super.unittest.main()
