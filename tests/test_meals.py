import unittest
from app import app
from api.resources.meals import Meal

"""This class contains unit tests for the meal apis and functions"""
class MealTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()
       
        self.meal_list = {
            'id': 1,
            'name': u'Posho & Meat',
            'price': 10.5
        }

    
    def test_api_create_meal(self):
        # Test API can create a meal option
        res = self.client.post('/api/v1/meals/', data=self.meal_list)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Posho & Meat', str(res.data))

    def test_api_get_meals(self):
        #Test API can get a meal with GET request
        res = self.client.get('/api/v1/meals/')
        self.assertEqual(res.status_code, 200)

    def test_api_update_meal(self):
        #Test API can edit an existing order with PUT request
        res = self.client.post('/api/v1/meals/',data={'meals': [1,3,2]})
        self.assertEqual(res.status_code, 201)
        rs = self.client.put('/api/v1/meals/1', data={'meals': [4]})
        self.assertEqual(rs.status_code, 200)
        results = self.client.get('api/v1/meals/1')
        self.assertIn([4], str(results.data))

    def test_api_delete_meal(self):
        #Test API can delete an existing meal with DELETE request
        res = self.client.post('/api/v1/meals/',data={'name': u'Posho & Meat'})
        self.assertEqual(res.status_code, 201)
        res = self.client.delete('/api/v1/meals/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client.get('/api/v1/meals/1')
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    unittest.main()