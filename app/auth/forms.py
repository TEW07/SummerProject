from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User
import re

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.common_passwords = self.load_common_passwords('app/data/top-10000-pass.txt')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')

    @staticmethod
    def load_common_passwords(file_path):
        with open(file_path, 'r') as file:
            common_passwords = set(line.strip() for line in file)
        return common_passwords

    def validate_password(self, password):
        # Check against commonly-used passwords
        if password.data in self.common_passwords:
            raise ValidationError('This password is too common. Please choose a different one.')

        # Check for repetitive or sequential characters
        if re.search(r'(.)\1{2,}', password.data):
            raise ValidationError('Password contains repetitive characters. Please choose a different one.')
        if re.search(r'(012|123|234|345|456|567|678|789)', password.data):
            raise ValidationError('Password contains sequential characters. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Username does not exist')


