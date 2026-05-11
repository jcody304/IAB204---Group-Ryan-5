
# Imports Flask Utilities: Blueprint (Group Related Routes), request (Access HTTP Request Data), redirect (Redirect Users to Another Route), url_for( Dynamically buils URLs for Routes)
from flask import Blueprint, render_template, request, redirect, url_for
# Imports login_user
from flask_login import login_user, logout_user
from .models import User
# Import form classes
from .forms import LoginForm, RegisterForm
from . import db

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
            return redirect(url_for('mainbp.index'))  # Redirect to the main page as logged in User
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
            return render_template('auth/register.html', form=form)
        user = User(email=form.email.data, role='customer') # Creates New User
        user.set_password(form.password.data) # Hash and Store Password

        # Save user to database
        db.session.add(user)
        db.session.commit()

        print('Registration successful!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

# Route to handle user logout
@authbp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('mainbp.index'))