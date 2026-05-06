# Creates and configures the Flask Application. THE ORDER OF THE FOLLOWING IMPORTS IS IMPORTANT, DO IT EXACTLY THE SAME!!!

# Import the main Flask class
from flask import Flask
# Import bootstrap support for Flask templates
from flask_bootstrap import Bootstrap5
# Import LoginManager to manage user login sessions
from flask_login import LoginManager
# Import os for interacting with native operating system and handle file paths
import os
# Import SQLAlchemy for Database Support (pip install Flask-SQLAlchemy)
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
# Import the User model used by Flask-Login
from .models import User
from .views import mainbp
from .events import eventbp
from .auth import authbp

# Function to create, configure, and return the Flask app
def create_app():
    app = Flask(__name__) # Create the Flask application instance
    bootstrap = Bootstrap5(app) # Initialise Bootstrap for use in templates
    app.secret_key = 'secretkey' # Secret key used for sessions, CSRF protection, and form security

    # Confiured LoginManager
    login_manager = LoginManager() # Create LoginManager instance
    login_manager.init_app(app) # Connect LoginManager to the Flask app

    # Configured DB Manager
    os.makedirs(app.instance_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(app.instance_path, 'events.db') # DB configuration for the app
    db.init_app(app) # Initialize the database with Flask app

    # Location to store images. !!!UNSURE IF IT WORKS!!!!
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Unhash the below lines one time to create DB if needed, then rehash them
    #with app.app_context():
        #db.create_all()

    # User loader function requred by Flask-Login. Tells Flask-Login how to reload a user from a stored session ID
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    #Import blueprints after the app is created
    from .views import mainbp
    from .events import eventbp 
    
    app.register_blueprint(mainbp) # Register the main blueprint
    app.register_blueprint(eventbp) # Register the events blueprint
    app.register_blueprint(authbp) # Register the auth blueprint
    
    # Return the configured Flask app
    return app

