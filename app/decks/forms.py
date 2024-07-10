from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreateDeckForm(FlaskForm):
    name = StringField('Deck Name', validators=[DataRequired()])
    submit = SubmitField('Create Deck')
