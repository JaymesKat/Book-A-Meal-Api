from api.__init__ import app
from api.app import setup_routes

setup_routes()

if __name__ == '__main__':
    app.run()