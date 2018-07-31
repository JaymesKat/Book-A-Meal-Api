import json
from tests.test_base_case import BaseTest


class MealTestCase(BaseTest):
    '''This class contains unit tests for the meal apis and functions'''

    def test_api_caterer_create_meal(self):
        ''' Test API - a caterer can create meal options'''       
        response = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(
                {
                    "name": "Posho & Peas",
                    "price": "11.5"}),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token
                )
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('Posho & Peas', str(response.data))

    def test_api_caterer_get_meals(self):
        ''' Test API - a caterer can get all meals '''

        response = self.client.get(
            '/api/v1/meals/',
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token))
        self.assertEqual(response.status_code, 200)

    def test_api_caterer_update_meal(self):
        '''
        Test API - a caterer can edit an existing order with PUT request
        '''
        res = self.client.post('/api/v1/meals/',
                               data=json.dumps({
                                   "name": "Spaghetti & Meat",
                                   "price": "15.5"}),
                               content_type='application/json',
                               headers=dict(
                                   Authorization='JWT ' +
                                   self.caterer_token))

        response_data = json.loads(res.data.decode())
        meal_id = response_data['Meal']['id']

        rs = self.client.put('/api/v1/meals/' +
                             str(meal_id),
                             data=json.dumps({
                                "name": "Spaghetti & Cheese",
                                "price": "13.5"}),
                             content_type='application/json',
                             headers=dict(
                                Authorization='JWT ' +
                                self.caterer_token))

        self.assertEqual(rs.status_code, 200)

        # check for updated meal info
        results = self.client.get(
            '/api/v1/meals/' +
            str(meal_id),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token))

        self.assertIn('Spaghetti & Cheese', str(results.data))

    def test_api_caterer_delete_meal(self):
        '''
        Test API a caterer can delete an existing meal with DELETE request    
        '''

        res = self.client.post('/api/v1/meals/',
                               data=json.dumps(
                                   {
                                    'name': 'Posho & Meat',
                                    'price': '9.0'
                                   }),
                               content_type='application/json',
                               headers=dict(
                                   Authorization='JWT ' + self.caterer_token))

        self.assertEqual(res.status_code, 201)
        response_data = json.loads(res.data.decode())
        meal_id = response_data['Meal']['id']

        res = self.client.delete(
            '/api/v1/meals/' +
            str(meal_id),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token))

        self.assertEqual(res.status_code, 202)

        # Test to see if it does not exist, should return a 404
        result = self.client.get(
            '/api/v1/meals/' +
            str(meal_id),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token))
        self.assertEqual(result.status_code, 404)

    def test_api_customer_should_not_create_meal(self):
        ''' Test API can create a meal option for non caterer'''
        response = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(
                {
                    "name": "Posho & Peas",
                    "price": "11.5"}),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.customer_token))
        self.assertEqual(response.status_code, 403)
        self.assertIn(
            'You must be an admin to access this resource', str(
                response.data))

    def test_customer_should_not_get_meals(self):
        ''' Test API - a customer should not be able to get meals'''

        response = self.client.get(
            '/api/v1/meals/',
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.customer_token))

        self.assertEqual(response.status_code, 403)
        self.assertIn(
            'You must be an admin to access this resource', str(
                response.data))

    def test_cannot_add_duplicate_meal_name(self):
        ''' Test API - a caterer can create meal options'''

        meal = {"name": "Ugali",
                "price": "15.5"}

        res = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(meal),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token))

        self.assertEqual(res.status_code, 201)
        self.assertIn('Ugali', str(res.data))

        second_res = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(meal),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token))

        self.assertEqual(second_res.status_code, 409)
        self.assertIn("Duplicate, enter a unique meal name",
                      str(second_res.data))

    def test_request_should_not_have_missing_field(self):
        ''' Test API - it should not create a meal with a missing field '''

        response = self.client.post(
            '/api/v1/meals/',
            data=json.dumps(
                {
                    "name": "Posho & Peas",
                }),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token))
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Missing fields: enter meal name and price', str(
                response.data))


if __name__ == "__main__":
    super.unittest.main()
