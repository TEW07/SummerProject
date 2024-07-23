from flask import render_template, url_for, flash, redirect, session
from . import auth_blueprint
from app.auth.forms import RegistrationForm, LoginForm
from .models import User, LoginEvent
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from app import db


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to sign in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)


from datetime import datetime, timedelta

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash('Sign in successful', 'success')

            # Update the last_login column
            user.last_login = datetime.utcnow()

            # Log the login event
            login_event = LoginEvent(user_id=user.user_id)
            db.session.add(login_event)
            db.session.commit()

            return redirect(url_for('main.dashboard'))
        else:
            flash('Sign in unsuccessful', 'danger')
    return render_template('login.html', title='Sign In', form=form)





@auth_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    flash(f'{current_user.username} Logged Out', 'success')
    logout_user()
    return redirect(url_for('auth.login'))
