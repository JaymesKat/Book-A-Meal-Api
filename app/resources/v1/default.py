import datetime
from flask import Flask, render_template, make_response
from flask_restful import Resource


class DefaultResource(Resource):
    
    def get(self):
        ''' Index route '''
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)