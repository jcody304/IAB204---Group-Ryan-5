# Defines all web forms using Flask-WTF. Froms are used to collect user input from the frontend.

# Import Flaskform, which is the case class for all forms in Flask-WTF (pip install Flask-WTF)
from flask_wtf import FlaskForm
# Import different types of file fields and rules
from flask_wtf.file import FileField, FileRequired, FileAllowed
# Import different types of form fields
from wtforms.fields import DateTimeLocalField, IntegerField, SelectField, TextAreaField, SubmitField, StringField, PasswordField
# Import validators to enforce input rules
from wtforms.validators import InputRequired, EqualTo, NumberRange, Optional

ALLOWED_FILE = ['png', 'jpg', 'jpeg', 'bmp']

# Form for creating a new destination
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    organisation_name = StringField('Organisation Name', validators=[Optional()])
    date = DateTimeLocalField('Date', validators=[InputRequired()])
    address = StringField('Location', validators=[InputRequired()])
    state_territory = SelectField('State/Territory',
        choices=[('', 'Choose...'),('ACT', 'ACT'),('NSW', 'NSW'),('NT', 'NT'),('QLD', 'QLD'),('TAS', 'TAS'),('VIC', 'VIC')],
        validators=[InputRequired()])
    postcode = IntegerField('Zip', validators=[InputRequired(), NumberRange(min=1000, max=9999, message="Postcode must be a 4 digit number")])
    category = SelectField('Category',
        choices=[(' ',' Select Category'),('music', 'Music'),('sports', 'Sports'),('theatre', 'Theatre'),('community', 'Community'),('education', 'Education')],
        validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    image = FileField('Cover Image', 
            validators=[FileRequired(message='Please Select a File'), FileAllowed(ALLOWED_FILE, message='Support only png, jpg, jpeg, bmp')])
    price = IntegerField('Price ($)', 
            validators=[InputRequired(), NumberRange(min=0, message="Price must be a positive number")])
    tickets_available = IntegerField('Tickets Available', 
            validators=[InputRequired(), NumberRange(min=0, message="Tickets available must be a positive number")])
    submit = SubmitField('Publish')

# Form for User Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    # back = SubmitField('Back')
    submit = SubmitField('Login')

# Form for User Registration
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    address = StringField('Address', validators=[InputRequired()])
    state_territory = SelectField('State/Territory',
        choices=[('', 'Choose...'),('ACT', 'ACT'),('NSW', 'NSW'),('NT', 'NT'),('QLD', 'QLD'),('TAS', 'TAS'),('VIC', 'VIC')],
        validators=[InputRequired()])
    postcode = IntegerField('Zip', validators=[InputRequired(), NumberRange(min=1000, max=9999, message="Postcode must be a 4‑digit number")])
    # back = SubmitField('Back')
    submit = SubmitField('Register')

# Form for Submitting Comments
class CommentForm(FlaskForm): 
    text = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Submit Comment')

# Form for Purchasing Tickets
class TicketPurchaseForm(FlaskForm):
    nameofattendee = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    state_territory = SelectField('State/Territory',
        choices=[('', 'Choose...'),('ACT', 'ACT'),('NSW', 'NSW'),('NT', 'NT'),('QLD', 'QLD'),('TAS', 'TAS'),('VIC', 'VIC')],
        validators=[InputRequired()])
    postcode = IntegerField('Zip', validators=[InputRequired(), NumberRange(min=1000, max=9999, message="Postcode must be a 4‑digit number")])
    ticketsAvailable = IntegerField('Tickets (Max 3)',
        validators=[InputRequired(), NumberRange(min=1, max=3)])
    submit = SubmitField('Buy')