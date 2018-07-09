from flask import render_template
from . import default

@default.route('/', methods=['GET'])
def index():
    return render_template('index.html')