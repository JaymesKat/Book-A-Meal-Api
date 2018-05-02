
import json
import unittest
from api.app import app

"""This class contains unit tests for the menu apis and functions"""
class MenuTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()
      
        self.menu_list = json.dumps({
            'meal_ids': [4, 2]
        })

    def test_api_setup_menu(self):
        # Test API can create a meal option
        res = self.client.post('/bookameal/api/v1/menu/', data=self.menu_list)
        self.assertEqual(res.status_code, 201)
        self.assertIn('4', str(res.data))

    def test_api_get_menu(self):
        #Test API can get menu with GET request
        res = self.client.get('bookameal/api/v1/menu/')
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()