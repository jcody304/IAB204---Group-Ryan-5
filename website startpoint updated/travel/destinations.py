from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination, Comment
from datetime import datetime
from .forms import DestinationForm, LoginForm, RegisterForm, CommentForm

destbp = Blueprint('destinations', __name__, url_prefix='/destinations')

def get_destination():
    # This is a placeholder implementation - replace with actual destination retrieval logic
    comments = [
        Comment("Alice", "Great place!", datetime(2023, 10, 1)),
        Comment("Bob", "Amazing experience!", datetime(2023, 10, 2))
    ]
    Brazil = Destination("Brazil", "A beautiful country with diverse culture and stunning landscapes.", 
                         "https://cdn.britannica.com/22/266122-050-DC806202/statue-Christ-the-Redeemer-Rio-de-Janiero-Brazil.jpg",
                         "BRL", comments
    )
    return Brazil

@destbp.route('/<id>')
def show(id):
    destination = get_destination()
    form = CommentForm()
    return render_template('destinations/show.html', destination=destination, form=form)

@destbp.route('/<id>/comment', methods=['GET', 'POST'])
def add_comment(id):
    form = CommentForm()
    if form.validate_on_submit():
        print(f'The following comment was posted: {form.text.data}')
    return redirect(url_for('destinations.show', id=id))

@destbp.route('/create', methods=['GET', 'POST'])
def create():
    print('Method:', request.method)
    form = DestinationForm()
    if form.validate_on_submit():
        print('Form created successfully!')
        return redirect(url_for('main.index'))  # Redirect to the show page for the new destination
    return render_template('destinations/create.html', form=form)

@destbp.route('/login', methods=['GET', 'POST'])
def login():
    print('Method:', request.method)
    login = LoginForm()
    if login.validate_on_submit():
        print('Login successfully!')
        return redirect(url_for('main.index'))  # Redirect to the show page for the new destination
    return render_template('destinations/login.html', form=login)

@destbp.route('/register', methods=['GET', 'POST'])
def register():
    print('Method:', request.method)
    register = RegisterForm()
    if register.validate_on_submit():
        print('Registration successful!')
        return redirect(url_for('main.index'))  # Redirect to the show page for the new destination
    return render_template('destinations/register.html', form=register)

        