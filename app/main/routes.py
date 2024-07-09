from flask import render_template
from . import main_blueprint
from flask_login import current_user


@main_blueprint.route('/')
def index():
    return render_template('home.html')


@main_blueprint.route('/decks')
def decks():
    return render_template('decks.html')

@main_blueprint.route('/deck')


@main_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html', username=current_user.username)


