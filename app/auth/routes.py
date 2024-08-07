from flask import render_template, url_for, flash, redirect, session, request
from . import auth_blueprint
from app.auth.forms import RegistrationForm, LoginForm
from app.gamification.routes import check_achievements
from .models import User, LoginEvent
from flask_login import login_user, login_required, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from datetime import datetime, timedelta
from app import db

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

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


def login_key():
    username = request.form.get('username')
    if username:
        return f"{get_remote_address()}:{username}"
    return get_remote_address()


@auth_blueprint.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute", key_func=login_key)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)

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

            points_awarded = 0
            detailed_message = ""

            # Check if user has already logged in today
            if today not in login_dates:
                # Update user points
                base_points = 10
                streak_points = streak * base_points  # Amplify points for streak
                points_awarded = streak_points

                # Ensure points is not None
                if user.points is None:
                    user.points = 0

                user.points += streak_points
                db.session.commit()

                check_achievements(current_user)

                # Create detailed message
                if streak == 1:
                    detailed_message = f"You've been awarded {base_points} points! Come back tomorrow to start a streak and earn more points."
                else:
                    detailed_message = f"You've been awarded {streak_points} points! (Streak: {streak} days, {base_points} points per day)"

            # Log the login event
            now = datetime.utcnow()
            login_event = LoginEvent(user_id=user.user_id, timestamp=now)
            db.session.add(login_event)
            db.session.commit()

            # Store streak in session
            session['streak'] = streak

            if points_awarded > 0:
                flash(f"Sign in successful! {detailed_message}", 'success')
            else:
                flash('Sign in successful! No points awarded as you have already logged in today.', 'success')

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



