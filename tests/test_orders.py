
import unittest
from app import app
from api.resources.orders import Order

"""This class contains unit tests for the menu apis and functions"""
class MenuTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()
        self.order = {
            'id': 8,
            'meal_id': 5,
            'date_submitted' : u'2018-04-24'
        }

    def test_api_create_order(self):
        # Test API can create an order
        res = self.client.post('/api/v1/orders/', data=self.order)
        self.assertEqual(res.status_code, 201)
        self.assertIn([1], str(res.data))

    def test_api_get_orders(self):
        #Test API can get an order with GET request
        res = self.client.get('/api/v1/orders/')
        self.assertEqual(res.status_code, 200)

    def test_api_update_order(self):
        #Test API can edit an existing order with PUT request
        res = self.client.post('/api/v1/orders/',data={'meal_id': 7})
        self.assertEqual(res.status_code, 201)
        rs = self.client.put('/api/v1/orders/1', data={'meal_id': 8})
        self.assertEqual(rs.status_code, 200)
        results = self.client.get('api/v1/orders/1')
        self.assertIn(8, str(results.data))

    def test_api_delete_order(self):
        #Test API can delete an existing order with DELETE request
        res = self.client.post('/api/v1/orders/',data={'meal_id': 8})
        self.assertEqual(res.status_code, 201)
        res = self.client.delete('/api/v1/orders/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client.get('/api/v1/orders/1')
        self.assertEqual(result.status_code, 404)

if __name__ == "__main__":
    unittest.main()