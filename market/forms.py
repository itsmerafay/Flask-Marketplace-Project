# We have made this form and it will go towards routes then from there with the data to register page like all the data  

from market.models import db, User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username Already Exists !! Try a different one.')

    def validate_email_address(self,email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Already Exists !! Try a different one.')

    username = StringField(label='User Name : ', validators=[Length(min=5, max=30), DataRequired()]) # .data will go from here when user enter into the field and submit 
    email_address = StringField(label = 'Email : ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label = 'Password ', validators=[Length(min=5, max=50), DataRequired()])
    password2 = PasswordField(label = 'Confirm Password : ', validators = [EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name : ', validators=[DataRequired()])
    password = PasswordField(label='Password : ', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label = "Purchase Item !!")
    
class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell Item !!")