import unittest
import os
import json
from flask import Flask

class BookAMealTestCase(unittest.TestCase):
    def setUp(self):
        self.app =  Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client
        self.order_list = {
            'id': 2,
            'meals': [1],
            'date_submitted' : u'2018-04-24'
        }

        self.meal_list = {
            'id': 1,
            'name': u'Posho & Meat',
            'price': 10.5
        }

        self.menu_list = {
            'meal_ids': [4,2]
        }

    
    def test_order_create(self):
        # Test API can create an order
        res = self.client().post('/api/v1/orders/', data=self.order_list)
        self.assertEqual(res.status_code, 201)
        self.assertIn([1], str(res.data))

    def test_meal_create(self):
        # Test API can create a meal option
        res = self.client().post('/api/v1/meals/', data=self.meal_list)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Posho & Meat', str(res.data))

    def test_menu_setup(self):
        # Test API can create a meal option
        res = self.client().post('/api/v1/menu/', data=self.menu_list)
        self.assertEqual(res.status_code, 201)
        self.assertIn([2,4], str(res.data))

    def test_get_all_orders(self):
        #Test API can get an order with GET request
        res = self.client().post('/api/v1/orders/', data=self.order_list)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/orders/')
        self.assertEqual(res.status_code, 200)
        self.assertIn([1], str(res.data))

    def test_get_all_meals(self):
        #Test API can get a meal with GET request
        res = self.client().post('/api/v1/meals/', data=self.meal_list)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/meals/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Posho & Meat', str(res.data))

    def test_get_menu(self):
        #Test API can get menu with GET request
        res = self.client().post('/api/v1/menu/', data=self.menu_list)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/menu/')
        self.assertEqual(res.status_code, 200)
        self.assertIn([2,4], str(res.data))

    def test_api_get_order_by_id(self):
        #Test API can get a single order by using id.
        res = self.client().post('/api/v1/orders/', data=self.order_list)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/orders/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn([1], str(res.data))

    def test_api_get_meal_by_id(self):
        #Test API can get a single meal by using id.
        res = self.client().post('/api/v1/meals/', data=self.meal_list)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/meals/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Posho & Meat', str(res.data))

    def test_edit_order(self):
        #Test API can edit an existing order with PUT request
        res = self.client().post('/api/v1/orders/',data={'meals': [1,3,2]})
        self.assertEqual(res.status_code, 201)
        res = self.client().put('/api/v1/orders/1', data={'meals': [4]})
        self.assertEqual(res.status_code, 200)
        results = self.client().get('api/v1/orders/1')
        self.assertIn([4], str(results.data))

    def test_edit_meal(self):
        #Test API can edit an existing meal option with PUT request
        res = self.client().post('/api/v1/meals/',data={'name': u'Posho & Meat'})
        self.assertEqual(res.status_code, 201)
        res = self.client().put('/api/v1/meals/1', data={'name': u'Spaghetti & Fish'})
        self.assertEqual(res.status_code, 200)
        results = self.client().get('api/v1/meals/1')
        self.assertIn('Spaghetti & Fish', str(results.data))

    def test_delete_order(self):
        #Test API can delete an existing order with DELETE request
        res = self.client().post('/api/v1/orders/',data={'meals': [1,3,2]})
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/orders/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/api/v1/orders/1')
        self.assertEqual(result.status_code, 404)

    def test_delete_meal(self):
        #Test API can delete an existing meal with DELETE request
        res = self.client().post('/api/v1/meals/',data={'name': u'Posho & Meat'})
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/meals/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/api/v1/meals/1')
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
        unittest.main()

