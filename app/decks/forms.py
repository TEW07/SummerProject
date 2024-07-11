from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class CreateDeckForm(FlaskForm):
    name = StringField('Deck Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Create Deck')


class AddCardForm(FlaskForm):
    front = StringField('Front', validators=[DataRequired()])
    back = StringField('Back', validators=[DataRequired()])
    deck = SelectField('Deck', coerce=int)
    submit = SubmitField('Add Card')


class EditCardForm(FlaskForm):
    front = StringField('Front', validators=[DataRequired()])
    back = StringField('Back', validators=[DataRequired()])
    submit = SubmitField('Update Card')

