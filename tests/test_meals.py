import unittest
import json
from api.app import app

"""This class contains unit tests for the meal apis and functions"""
class MealTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()
       
        self.meal = json.dumps({
            "name": "Posho & Meat",
            "price": "10.5"
        })

    def test_api_create_meal(self):
        # Test API can create a meal option
        res = self.client.post('/bookameal/api/v1/meals/', data=self.meal)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Posho & Meat', str(res.data))

    def test_api_get_meals(self):
        #Test API can get a meal with GET request
        res = self.client.get('/bookameal/api/v1/meals/')
        self.assertEqual(res.status_code, 200)

    def test_api_update_meal(self):
        #Test API can edit an existing order with PUT request
        res = self.client.post('/bookameal/api/v1/meals/',data=json.dumps({"name": "Spaghetti & Meat","price": "15.5"}))
        self.assertEqual(res.status_code, 201)
        inserted_meal_id = res['id']
        rs = self.client.put('/bookameal/api/v1/meals/'+inserted_meal_id, data=json.dumps({"name": "Spaghetti & Cheese","price": "13.5"}))
        self.assertEqual(rs.status_code, 200)
        results = self.client.get('/bookameal/api/v1/meals/'+inserted_meal_id)
        self.assertIn([4], str(results.data))

    def test_api_delete_meal(self):
        #Test API can delete an existing meal with DELETE request
        res = self.client.post('/bookameal/api/v1/meals/',data={'name': 'Posho & Meat', 'price': 9.0})
        self.assertEqual(res.status_code, 201)
        res = self.client.delete('/bookameal/api/v1/meals/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client.get('/bookameal/api/v1/meals/1')
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    unittest.main()