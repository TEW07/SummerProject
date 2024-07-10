from flask import render_template
from . import main_blueprint

from flask_login import current_user


@main_blueprint.route('/')
def index():
    return render_template('home.html')


@main_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html', username=current_user.username,
                           log_count=current_user.get_login_count(current_user.user_id),
                           log_latest=current_user.get_latest_login(current_user.user_id))


