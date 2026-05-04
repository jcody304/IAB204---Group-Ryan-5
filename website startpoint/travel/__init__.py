from flask import Flask
from flask_bootstrap5 import Bootstrap

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.secret_key = 'secretkey'

    #add Blueprints
    from . import views, destinations
    app.register_blueprint(views.mainbp)
    app.register_blueprint(destinations.destbp)

    return app

