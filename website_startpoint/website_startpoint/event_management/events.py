# Imports Flask Utilities: Blueprint (Group Related Routes), request (Access HTTP Request Data), redirect (Redirect Users to Another Route), url_for( Dynamically buils URLs for Routes)
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
# Imports DB
from . import db
# Import Custom Models
from .models import Event, Comment, EventImage, Location, Booking
# Import datetime for timestamp creating on comments
from datetime import datetime
# Import form classes
from .forms import EventForm, CommentForm, TicketPurchaseForm, EventEditForm
# Import os for interacting with native operating system and handle file paths
import os
# Imports secure_filename to safely upload file names
from werkzeug.utils import secure_filename

from flask_login import current_user, login_required

from uuid import uuid4

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
@login_required
def create():
    print('Method:', request.method)
    form = EventForm()
    if current_user.role != 'vendor':
        flash('Please login as a vendor to create an event.', 'danger')
        return redirect(url_for('mainbp.index'))
    form = EventForm()
    if form.validate_on_submit():
        try: 
            print('Form created successfully!')

            location = Location(address=form.address.data, state_territory=form.state_territory.data, postcode=form.postcode.data)
            db.session.add(location)
            db.session.flush()
            
            # Default acknowledgement statement logic
            acknowledgement_statement = form.acknowledgement_statement.data

            if form.acknowledgement_type.data == 'none':
                acknowledgement_statement = None

            elif form.acknowledgement_type.data == 'generic':
                acknowledgement_statement = ('We acknowledge the Traditional Custodians of the land on which this event takes place''and pay our respects to Elders past and present.')
            
            event = Event(name=form.name.data, organisation_name=form.organisation_name.data, date=form.date.data, category=form.category.data, 
                        description=form.description.data, location_id=location.id, price=form.price.data, tickets_available=form.tickets_available.data,
                        vendor_id=current_user.id, acknowledgement_type=form.acknowledgement_type.data, acknowledgement_traditional_custodians=form.acknowledgement_traditional_custodians.data, acknowledgement_statement=acknowledgement_statement, acknowledgement_researched=form.acknowledgement_researched.data, acknowledgement_not_welcome=form.acknowledgement_not_welcome.data, acknowledgement_respectful=form.acknowledgement_respectful.data)           
            db.session.add(event)
            db.session.flush() # Gives event an id before commit

            file = request.files.get('image')
            
            if file and file.filename:
                original_filename = secure_filename(file.filename) # Makes filenames secure
                unique_filename = f"{uuid4().hex}_{original_filename}" # Creates a unique filename so uploads do not overwrite each other
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename) # Builds file path using configured upload folder
                file.save(filepath)

                image = EventImage(filename='img/' + unique_filename, event_id=event.id)
                db.session.add(image)

            db.session.commit()
            flash('Event created successfully.', 'success')
            return redirect(url_for('mainbp.index'))  # Redirect to the show page for the new destination
        except Exception as e:
            db.session.rollback()
            flash('Something went wrong while creating the event.', 'danger')
            print(e)
    return render_template('events/create.html', form=form)

# Route for Categories
@eventbp.route('/category/<category>')
def category(category):
    events = Event.query.filter_by(category=category).order_by(Event.date.asc()).all()
    return render_template('index.html', events=events, featured_events=events[:4], selected_category=category)

# Route to Update Events
@eventbp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):

    event = Event.query.get_or_404(id)

    # Prevent non-vendors
    if current_user.role != 'vendor':
        flash('Only vendors can update events.', 'danger')
        return redirect(url_for('mainbp.index'))

    # Prevent editing other vendor events
    if event.vendor_id != current_user.id:
        flash('You can only edit your own events.', 'danger')
        return redirect(url_for('events.show', id=id))

    # Use the EventEditForm for editing, which restricts what fields can be changed
    form = EventEditForm()

    # Pre-fill form with current values
    if request.method == 'GET':
        form.date.data = event.date
        form.description.data = event.description
        form.status.data = event.status
        form.acknowledgement_type.data = event.acknowledgement_type
        form.acknowledgement_traditional_custodians.data = event.acknowledgement_traditional_custodians
        form.acknowledgement_statement.data = event.acknowledgement_statement
        form.acknowledgement_researched.data = event.acknowledgement_researched
        form.acknowledgement_not_welcome.data = event.acknowledgement_not_welcome
        form.acknowledgement_respectful.data = event.acknowledgement_respectful

    if form.validate_on_submit():
        # If in edit mode, only allow changes to specific fields
        event.date = form.date.data
        event.description = form.description.data
        event.status = form.status.data
        
        # Update acknowledgement fields
        event.acknowledgement_type = form.acknowledgement_type.data
        event.acknowledgement_traditional_custodians = form.acknowledgement_traditional_custodians.data
        event.acknowledgement_statement = form.acknowledgement_statement.data
        event.acknowledgement_researched = form.acknowledgement_researched.data
        event.acknowledgement_not_welcome = form.acknowledgement_not_welcome.data
        event.acknowledgement_respectful = form.acknowledgement_respectful.data

        db.session.commit()

        flash('Event updated successfully.', 'success')

        return redirect(url_for('events.show', id=id))

    return render_template('events/create.html', form=form, event=event, edit_mode=True)

# Route user to ticket purchase page
@eventbp.route('/<int:id>/purchase', methods=['GET', 'POST'])
@login_required
def purchase(id):

    event = Event.query.get_or_404(id)

    form = TicketPurchaseForm()

    if form.validate_on_submit():

        quantity = form.ticketsAvailable.data

        if quantity > event.tickets_remaining:
            flash('Not enough tickets remaining.', 'danger')
            return redirect(url_for('events.purchase', id=id))
        
        booking = Booking(quantity=quantity, total_price=quantity * event.price, user_id=current_user.id, event_id=event.id)

        db.session.add(booking)
        event.tickets_sold += quantity

        db.session.commit()

        flash(f'Tickets purchased successfully! You purchased {quantity} ticket{"s" if quantity != 1 else ""}', 'success')

        return redirect(url_for('events.show', id=id))

    return render_template('events/ticket_purchase.html', form=form, event=event)
# Route user to events history page
@eventbp.route('/history')
@login_required
def history():

    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()

    return render_template('events/event_history.html', bookings=bookings)

# Route for acknowlegement
@eventbp.route('/acknowledgement')
def acknowledgement():
    return render_template('events/acknowledgement.html')