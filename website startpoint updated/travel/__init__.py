from flask import Flask
from flask_bootstrap import Bootstrap5

def create_app():
    app = Flask(__name__)
    Bootstrap5(app)
    app.secret_key = 'secretkey'

    #add Blueprints
    from . import views, destinations
    app.register_blueprint(views.mainbp)
    app.register_blueprint(destinations.destbp)

    return app

