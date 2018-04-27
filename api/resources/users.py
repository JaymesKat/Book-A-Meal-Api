from flask import Flask, jsonify
from flask_restful import Resource

class User(Resource):

    users = [
    {
        'id': 1,
        'first_name': u'James',
        'last_name': u'Katarikawe',
        'email': u'jpkatarikawe@gmail.com',
        'password': u'james', 
        'isCaterer': False
    },
    {
        'id': 2,
        'first_name': u'Paul',
        'last_name': u'Kayongo',
        'email': u'paulkayongo@gmail.com',
        'password': u'kayongo', 
        'isCaterer': False
    },
    {
        'id': 3,
        'first_name': u'Joseph',
        'last_name': u'Odur',
        'email': u'odur@gmail.com',
        'password': u'odur', 
        'isCaterer': True
    },
    {
        'id': 4,
        'first_name': u'Phillip',
        'last_name': u'Seryazi',
        'email': u'seryazi@gmail.com',
        'password': u'seryazi', 
        'isCaterer': True
    }
]
    def add(self, user):
        self.users.append(user)
    