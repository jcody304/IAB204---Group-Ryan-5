# Defines routes related to destinations using Flask Blueprint

# Imports Flask Utilities: Blueprint (Group Related Routes), request (Access HTTP Request Data), redirect (Redirect Users to Another Route), url_for( Dynamically buils URLs for Routes)
from flask import Blueprint, render_template, request, redirect, url_for
# Imports DB
from . import db
# Import Custom Models
from .models import Event, Comment, EventImage
# Import datetime for timestamp creating on comments
from datetime import datetime
# Import form classes
from .forms import EventForm, CommentForm, TicketPurchaseForm
# Import os for interacting with native operating system and handle file paths
import os
# Imports secure_filename to safely upload file names
from werkzeug.utils import secure_filename
# Imports current app for find file path later
from flask import current_app

from flask_login import current_user, login_required

# Create Blueprint named 'events'. url_prefix means all routes in this file start with '/events'
eventbp = Blueprint('events', __name__, url_prefix='/events')

# Route to display a event based on its ID
@eventbp.route('/<int:id>')
def show(id):
    event = Event.query.get_or_404(id) # Retrieve event data
    form = CommentForm() # Create a comment form instance for this page
    return render_template('events/show.html', event=event, form=form) # Render the event page and pass data to the template

# Route to handle adding a comment to a destination. Suports both GET (Load Page), and POST (Submit Form)
@eventbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def add_comment(id):
    form = CommentForm() # Create form instance
    if form.validate_on_submit(): # Check if form is submitted and valid
        comment = Comment(text=form.text.data, user_id=current_user.id, event_id=id) # Saves comment to events.db
        db.session.add(comment)
        db.session.commit()
        print(f'The following comment was posted: {form.text.data}')
    return redirect(url_for('events.show', id=id)) # Redirect back to the events page after submission

# Route to create a new event
@eventbp.route('/create', methods=['GET', 'POST'])
def create():
    print('Method:', request.method)
    form = EventForm() 
    if form.validate_on_submit():
        print('Form created successfully!')

        # Saves img location to events.db
        event = Event(name=form.name.data, description=form.description.data, location=form.location.data, price=form.price.data)
        db.session.add(event)
        db.session.flush() # Gives event an id before commit

        files = request.files.getlist('image')
        
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename) # Makes filenames secure
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename) # Builds file path using configured upload folder
                file.save(filepath)

                image = EventImage(filename='img' + filename, event_id=event.id)
                db.session.add(image)

        db.session.commit()
        print('Saved Successfully')
        return redirect(url_for('mainbp.index'))  # Redirect to the show page for the new destination
    return render_template('events/create.html', form=form)

# Route user to events history page
@eventbp.route('/history')
def history():
    return render_template('events/event_history.html')

#Temp Route to be testing 
@eventbp.route('/purchase')
def purchase():
    form = TicketPurchaseForm()
    return render_template('events/ticket_purchase.html', form=form)


# The better Route to purchase tickets for an event to use once events are dynamically created and have their own pages. 
# This route will be linked to a "Purchase Tickets" button on each event's page. It will display a form to collect user information for ticket purchase and handle the form submission.
#@eventbp.route('/<id>/purchase', methods=['GET', 'POST'])
#def purchase_tickets(id):
#    form = TicketPurchaseForm()
#    if form.validate_on_submit():
#        print('Ticket purchase successful!')
#        print(f'Name: {form.nameofattendee.data}, Email: {form.email.data}, Phone: {form.phone.data}, Address: {form.address.data}, City: {form.city.data}')
#       return redirect(url_for('events.show', id=id))  # Redirect to the show page for the event after purchase
#    return render_template('events/ticket_purchase.html', form=form)