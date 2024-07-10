from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from app.decks.models import Deck


class CreateDeckForm(FlaskForm):
    name = StringField('Deck Name', validators=[DataRequired()])
    submit = SubmitField('Create Deck')


class AddCardForm(FlaskForm):
    front = StringField('Front', validators=[DataRequired()])
    back = StringField('Back', validators=[DataRequired()])
    deck = SelectField('Deck', coerce=int)  # Add coerce=int to ensure proper handling of deck IDs
    submit = SubmitField('Add Card')
