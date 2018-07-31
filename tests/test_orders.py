import datetime
import json
from tests.test_base_case import BaseTest

"""This class contains unit tests for the menu apis and functions"""


class OrderTestCase(BaseTest):

    def test_api_customer_create_order(self):
        # A customer can create an order

        res = self.client.post(
            '/api/v1/orders/',
            data=self.order,
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.customer_token))

        self.assertEqual(res.status_code, 201)
        res_data = json.loads(res.data.decode())

        order = json.loads(self.order)
        self.assertIn(str(order["meal_id"]), str(res_data['order']['meal_id']))

    def test_api_caterer_should_not_create_order(self):
        # A customer can create an order

        second_res = self.client.post(
            '/api/v1/orders/',
            data=json.dumps(
                self.order),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token))
        self.assertEqual(second_res.status_code, 403)
        self.assertIn(
            'An admin(caterer) is not allowed to post an order', str(
                second_res.data))

    def test_api_customer_should_not_get_orders(self):
        # Test API can get an order with GET request

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

    def test_api_customer_update_order(self):
        # Test API can edit an existing order with PUT request

        res = self.client.post(
            '/api/v1/orders/',
            data=self.order,
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.customer_token))

        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data.decode())

        new_order_id = data['order']['id']
        menu_list = json.loads(self.menu_list)

        rs = self.client.put('/api/v1/orders/' + str(new_order_id),
                             data=json.dumps(
                                 {'meal_id': menu_list["meal_ids"][2]}),
                             content_type='application/json',
                             headers=dict(
                                 Authorization='JWT ' + self.customer_token))

        self.assertEqual(rs.status_code, 202)

        results = self.client.get(
            '/api/v1/orders/' +
            str(new_order_id),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token))

        self.assertIn(str(new_order_id), str(results.data))

    def test_api_customer_delete_order(self):
        '''Test API can delete an existing order with DELETE request'''

        res = self.client.post(
            '/api/v1/orders/',
            data=self.order,
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.customer_token))

        self.assertEqual(res.status_code, 201)
        response_data = json.loads(res.data.decode())
        new_id = response_data['order']['id']

        res = self.client.delete(
            '/api/v1/orders/' +
            str(new_id),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.customer_token))

        self.assertEqual(res.status_code, 202)

        result = self.client.get(
            '/api/v1/orders/' +
            str(new_id),
            content_type='application/json',
            headers=dict(
                Authorization='JWT ' +
                self.caterer_token))

        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    super.unittest.main()
