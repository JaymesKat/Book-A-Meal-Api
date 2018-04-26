from flask_restful import Resource

class Order(Resource):

    orders = [
         {
            'id': 1,
            'meals': [1,2,3,4],
            'date_submitted' : u'2018-04-24'
        },
        {
            'id': 2,
            'meals': [1],
            'date_submitted' : u'2018-04-24'
        },
        {
            'id': 23,
            'meals': [1,4],
            'date_submitted' : u'2018-04-25'
        },
        {
            'id': 4,
            'meals': [1,3,4],
            'date_submitted' : u'2018-04-25'
        }
    ]

    def get(self):
        pass
    def post(self):
        pass