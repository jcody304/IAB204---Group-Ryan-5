# Imports Flask Utilities: Blueprint (Group Related Routes), request (Access HTTP Request Data), redirect (Redirect Users to Another Route), url_for( Dynamically buils URLs for Routes)
from flask import Blueprint, render_template, request, redirect, url_for, flash
# Imports login_user
from flask_login import login_user, logout_user, current_user, login_required
from .models import User
# Import form classes
from .forms import LoginForm, RegisterForm
from . import db
from datetime import datetime
from .models import Event, Booking

# Create Blueprint named 'auth'. url_prefix means all routes in this file start with '/auth'
authbp = Blueprint('auth', __name__, url_prefix='/auth')

# Route to handle user login
@authbp.route('/login', methods=['GET', 'POST'])
def login():
    print('Method:', request.method)
    form = LoginForm()
    if form.validate_on_submit():
        # Get form data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first() # Look up user in database
        if user and user.check_password(password): # Check if user exists and password matches
            login_user(user)
            print('Login successfully!')
            #Redirects the User back to the previous protected page
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('mainbp.index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)

# Route to handle user registration
@authbp.route('/register', methods=['GET', 'POST'])
def register():
    print('Method:', request.method)
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()  # Check if email already exists
        if existing_user:
            print('Email already registered')
            flash('Email already registered. Please use a different email or login.', 'danger')
            return render_template('auth/register.html', form=form)
        user = User(email=form.email.data, role=form.role.data) # Creates New User
        user.set_password(form.password.data) # Hash and Store Password

        # Save user to database
        db.session.add(user)
        db.session.commit()

        print('Registration successful!')
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

# Route to handle user logout
@authbp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('mainbp.index'))

# Route to views account details
@authbp.route('/account')
@login_required
def account():

    current_events = []
    past_events = []

    upcoming_bookings = []
    past_bookings = []
    all_bookings = []

    # Get all bookings for the current user
    all_bookings = Booking.query.filter(
        Booking.user_id == current_user.id
    ).order_by(Booking.created_at.desc()).all()

    if current_user.role == 'vendor':

        current_events = Event.query.filter(
            Event.vendor_id == current_user.id,
            Event.date >= datetime.now()
        ).order_by(Event.date.asc()).all()

        past_events = Event.query.filter(
            Event.vendor_id == current_user.id,
            Event.date < datetime.now()
        ).order_by(Event.date.desc()).all()

    elif current_user.role == 'customer':

        upcoming_bookings = Booking.query.join(Event).filter(
            Booking.user_id == current_user.id,
            Event.date >= datetime.now()
        ).order_by(Event.date.asc()).all()

        past_bookings = Booking.query.join(Event).filter(
            Booking.user_id == current_user.id,
            Event.date < datetime.now()
        ).order_by(Event.date.desc()).all()

    return render_template(
        'auth/account.html',
        current_events=current_events,
        past_events=past_events,
        upcoming_bookings=upcoming_bookings,
        past_bookings=past_bookings,
        all_bookings=all_bookings
    )