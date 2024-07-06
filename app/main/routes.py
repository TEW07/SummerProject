from flask import render_template
from . import main_blueprint


@main_blueprint.route('/')
def index():
    return render_template('home.html')


@main_blueprint.route('/decks')
def decks():
    return render_template('decks.html')


