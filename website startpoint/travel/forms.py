from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField
from wtforms.validators import InputRequired, Length

class DestinationForm(FlaskForm):
    name = StringField('Country', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    image = StringField('Cover Image', validators=[InputRequired()])
    currency = StringField('Currency', validators=[InputRequired()])
    submit = SubmitField('Create')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    confirm_password = StringField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Register')

class CommentForm(FlaskForm): 
    text = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Submit Comment')