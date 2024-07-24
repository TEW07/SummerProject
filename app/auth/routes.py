from flask import render_template, url_for, flash, redirect, session
from . import auth_blueprint
from app.auth.forms import RegistrationForm, LoginForm
from .models import User, LoginEvent
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
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


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash('Sign in successful', 'success')

            # Calculate the streak
            today = datetime.utcnow().date()
            yesterday = today - timedelta(days=1)
            login_events = LoginEvent.query.filter_by(user_id=user.user_id).order_by(LoginEvent.timestamp.desc()).all()
            login_dates = {event.timestamp.date() for event in login_events}

            streak = 1  # Default streak if today is the first login
            if yesterday in login_dates:
                expected_date = yesterday
                while expected_date in login_dates:
                    streak += 1
                    expected_date -= timedelta(days=1)

            # Check if user has already logged in today
            if today not in login_dates:
                # Update user points
                base_points = 10
                streak_points = streak * base_points  # Amplify points for streak

                # Ensure points is not None
                if user.points is None:
                    user.points = 0

                user.points += streak_points
                db.session.commit()

            # Log the login event
            now = datetime.utcnow()
            login_event = LoginEvent(user_id=user.user_id, timestamp=now)
            db.session.add(login_event)
            db.session.commit()

            # Store streak in session
            session['streak'] = streak

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


@auth_blueprint.route('/account_settings')
@login_required
def account_settings():
    return render_template('account_settings.html')


@auth_blueprint.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.user_id)
    if user:
        # Perform cascading deletions if necessary
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash('Your account has been deleted.', 'success')
        return redirect(url_for('main.index'))
    flash('Account deletion failed.', 'danger')
    return redirect(url_for('auth.account_settings'))