# Defines the data models used in the application. Represents the core objects of the system

# Imports datetime for timestamps
from datetime import datetime
# Imports DB from __initi__.py
from . import db
# Imports UserMixin providing default implementation for authentication-related methods. (pip install Flask-Login)
from flask_login import UserMixin
# Imports password hashing and checks for improved password security
from werkzeug.security import generate_password_hash, check_password_hash

# User class defined representing an authenticated User
class User(UserMixin, db.Model): # Inherits UserMixin to work with Flask-Login and db.Model for database assignment
    __tablename__ = 'users' # Assigns a tablename
    id = db.Column(db.Integer, primary_key=True) # Primary Key for each user
    email = db.Column(db.String(100), unique=True, nullable=False) # User Email Address
    role = db.Column(db.String(50), nullable=False, default='customer') # User role and sets it to default
    password_hash = db.Column(db.String(255), nullable=False) # Hashed Password
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')

    # Sets the user's password by hashing it
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check entered password against stored hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

# Event class defined representing an event
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(20))
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Open')
    price = db.Column(db.Float)
    images = db.relationship('EventImage', back_populates='event', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='event', cascade='all, delete-orphan')

# Comment class defined representing a user comment on a destination
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user = db.relationship('User', back_populates='comments')
    event = db.relationship('Event', back_populates='comments')

# Images class defined representing the images uploaded for events
class EventImage(db.Model):
    __tablename__ = 'event_images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    event = db.relationship('Event', back_populates='images')