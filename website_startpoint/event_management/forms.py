# Import Flaskform, which is the case class for all forms in Flask-WTF (pip install Flask-WTF)
from flask_wtf import FlaskForm
# Import different types of file fields and rules
from flask_wtf.file import FileField, FileRequired, FileAllowed
# Import different types of form fields
from wtforms.fields import DateTimeLocalField, IntegerField, SelectField, TextAreaField, SubmitField, StringField, PasswordField, BooleanField
# Import validators to enforce input rules
from wtforms.validators import InputRequired, EqualTo, NumberRange, Optional, Length, ValidationError, Email

import re
from datetime import datetime

ALLOWED_FILE = ['png', 'jpg', 'jpeg', 'bmp']

# Form for creating a new Event 
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
        choices=[(' ',' Select Category'),('music', 'Music'),('sports', 'Sports'),('theatre', 'Theatre'),('comedy', 'Comedy')],
        validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Cover Image', 
            validators=[FileRequired(message='Please Select a File'), FileAllowed(ALLOWED_FILE, message='Support only png, jpg, jpeg, bmp')])
    price = IntegerField('Price ($)', 
            validators=[InputRequired(), NumberRange(min=0, message="Price must be a positive number")])
    tickets_available = IntegerField('Tickets Available', 
            validators=[InputRequired(), NumberRange(min=0, message="Tickets available must be a positive number")])
    # Ackowledgement of Country and Custodians
    acknowledgement_type = SelectField('Acknowledgement of Country', choices=[('none', 'No Acknowledgement of Country'), ('generic', 'Acknowledgement of Country: generic'), ('enhanced', 'Acknowledgement of Country: enhanced')], validators=[InputRequired()])
    acknowledgement_traditional_custodians = StringField('Traditional Custodians / Traditional Owners', validators=[Optional()])
    acknowledgement_statement = TextAreaField('Custom Acknowledgement of Country Statement', validators=[Optional()])
    acknowledgement_researched = BooleanField('I have used reliable sources to research the Traditional Custodians.')
    acknowledgement_not_welcome = BooleanField('I understand this is an Acknowledgement of Country, not a Welcome to Country.')
    acknowledgement_respectful = BooleanField('I have checked that the statement is respectful, accurate, and not tokenistic.')
    
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        if self.acknowledgement_type.data == 'enhanced':
            valid = True
            if not self.acknowledgement_traditional_custodians.data:
                self.acknowledgement_traditional_custodians.errors.append('Please identify the Traditional Custodians for an enhanced Acknowledgement.')
                valid = False

            if not self.acknowledgement_statement.data:
                self.acknowledgement_statement.errors.append('Please write a custom Acknowledgement statement.')
                valid = False

            if not self.acknowledgement_researched.data:
                self.acknowledgement_researched.errors.append('Please confirm that you used reliable sources.')
                valid = False

            if not self.acknowledgement_not_welcome.data:
                self.acknowledgement_not_welcome.errors.append('Please confirm you understand the difference between an Acknowledgement and a Welcome to Country.')
                valid = False

            if not self.acknowledgement_respectful.data:
                self.acknowledgement_respectful.errors.append('Please confirm the statement is respectful and not tokenistic.')
                valid = False
            return valid
        elif self.acknowledgement_type.data == 'generic':
            valid = True
            if not self.acknowledgement_traditional_custodians.data:
                self.acknowledgement_traditional_custodians.errors.append('Please identify the Traditional Custodians for a generic Acknowledgement.')
                valid = False

            if not self.acknowledgement_researched.data:
                self.acknowledgement_researched.errors.append('Please confirm that you used reliable sources.')
                valid = False

            if not self.acknowledgement_not_welcome.data:
                self.acknowledgement_not_welcome.errors.append('Please confirm you understand the difference between an Acknowledgement and a Welcome to Country.')
                valid = False

            if not self.acknowledgement_respectful.data:
                self.acknowledgement_respectful.errors.append('Please confirm the statement is respectful and not tokenistic.')
                valid = False
            return valid
        return True
    submit = SubmitField('Publish')

# Form for editing an existing event - restricted fields only
class EventEditForm(FlaskForm):
    date = DateTimeLocalField('Date', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    status = SelectField('Event Status', 
        choices=[('Open', 'Open'), ('Inactive', 'Inactive'), ('Sold Out', 'Sold Out'), ('Cancelled', 'Cancelled')],
        validators=[InputRequired()])
    # Acknowledgement of Country - only type and traditional custodians can be modified
    acknowledgement_type = SelectField('Acknowledgement of Country', 
        choices=[('none', 'No Acknowledgement of Country'), ('generic', 'Acknowledgement of Country: generic'), ('enhanced', 'Acknowledgement of Country: enhanced')], 
        validators=[InputRequired()])
    acknowledgement_traditional_custodians = StringField('Traditional Custodians / Traditional Owners', validators=[Optional()])
    acknowledgement_statement = TextAreaField('Custom Acknowledgement of Country Statement', validators=[Optional()])
    acknowledgement_researched = BooleanField('I have used reliable sources to research the Traditional Custodians.')
    acknowledgement_not_welcome = BooleanField('I understand this is an Acknowledgement of Country, not a Welcome to Country.')
    acknowledgement_respectful = BooleanField('I have checked that the statement is respectful, accurate, and not tokenistic.')
    
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        if self.acknowledgement_type.data == 'enhanced':
            valid = True
            if not self.acknowledgement_traditional_custodians.data:
                self.acknowledgement_traditional_custodians.errors.append('Please identify the Traditional Custodians for an enhanced Acknowledgement.')
                valid = False

            if not self.acknowledgement_statement.data:
                self.acknowledgement_statement.errors.append('Please write a custom Acknowledgement statement.')
                valid = False

            if not self.acknowledgement_researched.data:
                self.acknowledgement_researched.errors.append('Please confirm that you used reliable sources.')
                valid = False

            if not self.acknowledgement_not_welcome.data:
                self.acknowledgement_not_welcome.errors.append('Please confirm you understand the difference between an Acknowledgement and a Welcome to Country.')
                valid = False

            if not self.acknowledgement_respectful.data:
                self.acknowledgement_respectful.errors.append('Please confirm the statement is respectful and not tokenistic.')
                valid = False
            return valid
        elif self.acknowledgement_type.data == 'generic':
            valid = True
            if not self.acknowledgement_traditional_custodians.data:
                self.acknowledgement_traditional_custodians.errors.append('Please identify the Traditional Custodians for a generic Acknowledgement.')
                valid = False

            if not self.acknowledgement_researched.data:
                self.acknowledgement_researched.errors.append('Please confirm that you used reliable sources.')
                valid = False

            if not self.acknowledgement_not_welcome.data:
                self.acknowledgement_not_welcome.errors.append('Please confirm you understand the difference between an Acknowledgement and a Welcome to Country.')
                valid = False

            if not self.acknowledgement_respectful.data:
                self.acknowledgement_respectful.errors.append('Please confirm the statement is respectful and not tokenistic.')
                valid = False
            return valid
        return True
    submit = SubmitField('Save Changes')

# Form for User Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

# Form for User Registration
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, message='Password must be at least 8 characters long')])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    role = SelectField('Account Type', choices=[('customer', 'Customer'), ('vendor', 'Vendor')], validators=[InputRequired()])
    submit = SubmitField('Register')
    def validate_password(self, field):
        password = field.data

        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter')

        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character')

# Form for Submitting Comments
class CommentForm(FlaskForm): 
    text = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Submit Comment')

# Form for Purchasing Tickets
class TicketPurchaseForm(FlaskForm):
    nameofattendee = StringField('Name', validators=[InputRequired()])
    ticketsAvailable = IntegerField('Tickets (Max 3)',
        validators=[InputRequired(), NumberRange(min=1, max=3)])
    submit = SubmitField('Buy')