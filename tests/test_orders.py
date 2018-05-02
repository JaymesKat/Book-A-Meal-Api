import datetime
import unittest
import json
from api.app import app

"""This class contains unit tests for the menu apis and functions"""
class OrderTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()
        self.order = json.dumps({
            'user_id': 8,
            'meal_id': 5
        })

    def test_api_create_order(self):
        # Test API can create an order
        res = self.client.post('/bookameal/api/v1/orders/', data=self.order)
        self.assertEqual(res.status_code, 201)
        today = datetime.date.today().strftime("%Y-%m-%d")
        self.assertIn(today, str(res.data))

    def test_api_get_orders(self):
        #Test API can get an order with GET request
        res = self.client.get('/bookameal/api/v1/orders/')
        self.assertEqual(res.status_code, 200)

    def test_api_update_order(self):
        #Test API can edit an existing order with PUT request
        res = self.client.post('/bookameal/api/v1/orders/',data=json.dumps({'meal_id':7, 'user_id': 8}))
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data.decode())
        new_order_id = data['order']['id']
        rs = self.client.put('/bookameal/api/v1/orders/'+str(new_order_id), data=json.dumps({'meal_id':5, 'user_id': 1}))
        self.assertEqual(rs.status_code, 200)
        results = self.client.get('/bookameal/api/v1/orders/'+str(new_order_id))
        self.assertIn('5', str(results.data))

    def test_api_delete_order(self):
        #Test API can delete an existing order with DELETE request
        res = self.client.post('/bookameal/api/v1/orders/',data=json.dumps({'meal_id':5, 'user_id': 1}))
        self.assertEqual(res.status_code, 201)
        response_data = json.loads(res.data.decode())
        new_id = response_data['order']['id']
        res = self.client.delete('/bookameal/api/v1/orders/'+str(new_id))
        self.assertEqual(res.status_code, 204)
        # Test to see if it exists, should return a 404
        result = self.client.get('/bookameal/api/v1/orders/'+str(new_id))
        self.assertEqual(result.status_code, 404)

if __name__ == "__main__":
    unittest.main()