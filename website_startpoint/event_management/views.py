# This is the main blueprint py. Defines the main routes (URLs) for the web application using Flask Blueprint
# The Blueprint allows routes to be organised into modular components instead of placing everything in a single file

# Import Blueprint to group routes, and render_template to display HTML Pages. (pip install Flask)
from flask import Blueprint, render_template 
# Import login and logout Functios from Flask-Login to manage user sessions. (pip install Flask-Login)
from flask_login import login_user
from flask_login import logout_user
# Import the User model
from .models import User, Event

# Create a Blueprint named mainbp. __name__ helps Flask locate resources like templates
mainbp = Blueprint('mainbp', __name__)

# Route for homepage. Function executes when user visits the root URL
@mainbp.route('/')
def index():
    events = Event.query.order_by(Event.date.asc()).all()
    featured_events = events[:4]
    return render_template('index.html', events=events, featured_events=featured_events) # Render and return the index.html