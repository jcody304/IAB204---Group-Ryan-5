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
    bookings = db.relationship('Booking', back_populates='user', cascade='all, delete-orphan')
    events = db.relationship('Event', backref='vendor', lazy=True)

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
    vendor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    organisation_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(20))
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='Open')
    price = db.Column(db.Float)
    images = db.relationship('EventImage', back_populates='event', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='event', cascade='all, delete-orphan')
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    location = db.relationship('Location', back_populates='events')
    tickets_available = db.Column(db.Integer, nullable=False)
    tickets_sold = db.Column(db.Integer, nullable=False, default=0)
    bookings = db.relationship('Booking', back_populates='event', cascade='all, delete-orphan')
    
    # Acknowledgement of Country and Custodians
    acknowledgement_type = db.Column(db.String(20), nullable=False, default='none')
    acknowledgement_traditional_custodians = db.Column(db.String(200), nullable=True)
    acknowledgement_statement = db.Column(db.Text, nullable=True)
    acknowledgement_researched = db.Column(db.Boolean, default=False)
    acknowledgement_not_welcome = db.Column(db.Boolean, default=False)
    acknowledgement_respectful = db.Column(db.Boolean, default=False)
    
    @property
    def tickets_remaining(self):
        return self.tickets_available - self.tickets_sold

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

# Locations class defined representing the locations of events
class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(150), nullable=False)
    state_territory = db.Column(db.String(10), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)

    events = db.relationship('Event', back_populates='location')
    
# Bookings class defined representing previous bookings
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)

    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    user = db.relationship('User', back_populates='bookings')
    event = db.relationship('Event', back_populates='bookings')