from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from app.decks.models import Deck


class CreateDeckForm(FlaskForm):
    name = StringField('Deck Name', validators=[DataRequired()])
    submit = SubmitField('Create Deck')


class AddCardForm(FlaskForm):
    front = StringField('Front', validators=[DataRequired(), Length(min=1, max=255)])
    back = StringField('Back', validators=[DataRequired(), Length(min=1, max=255)])
    deck_id = SelectField('Deck', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Card')

    def __init__(self, *args, **kwargs):
        super(AddCardForm, self).__init__(*args, **kwargs)
        self.deck_id.choices = [(deck.deck_id, deck.name) for deck in Deck.query.all()]
