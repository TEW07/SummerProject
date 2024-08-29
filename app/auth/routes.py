from datetime import datetime, timedelta

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.decks.models import Card, Deck
from app.gamification.utils import check_achievements
from app.review.models import ReviewOutcome

from . import auth_blueprint
from .models import LoginEvent, User

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to sign in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", title="Register", form=form)


def login_key():
    username = request.form.get("username")
    if username:
        return f"{get_remote_address()}:{username}"
    return get_remote_address()


@auth_blueprint.route("/login", methods=["GET", "POST"])
@limiter.limit("4 per minute", key_func=login_key)
@limiter.limit("7 per hour", key_func=login_key)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=True)

                today = datetime.utcnow().date()
                yesterday = today - timedelta(days=1)
                login_events = (
                    LoginEvent.query.filter_by(user_id=user.user_id)
                    .order_by(LoginEvent.timestamp.desc())
                    .all()
                )
                login_dates = {event.timestamp.date() for event in login_events}

                streak = 1
                if yesterday in login_dates:
                    expected_date = yesterday
                    while expected_date in login_dates:
                        streak += 1
                        expected_date -= timedelta(days=1)

                points_awarded = 0
                detailed_message = ""

                if today not in login_dates:
                    base_points = 10
                    streak_points = streak * base_points
                    points_awarded = streak_points

                    if user.points is None:
                        user.points = 0

                    user.points += streak_points
                    db.session.commit()

                    check_achievements(current_user)

                    if streak == 1:
                        detailed_message = (f"You've been awarded {base_points} points! Come back tomorrow to start a "
                                            f"streak and earn more points.")
                    else:
                        detailed_message = (f"You've been awarded {streak_points} points! (Streak: {streak} days, "
                                            f"{base_points} points per day)")

                now = datetime.utcnow()
                login_event = LoginEvent(user_id=user.user_id, timestamp=now)
                db.session.add(login_event)
                db.session.commit()

                session["streak"] = streak

                if points_awarded > 0:
                    flash(f"Sign in successful! {detailed_message}", "success")
                else:
                    flash(
                        "Sign in successful! No points awarded as you have already logged in today.",
                        "success",
                    )

                return redirect(url_for("main.dashboard"))
            else:
                flash("Sign in unsuccessful: Incorrect password.", "danger")
        else:
            flash("Sign in unsuccessful: Username does not exist.", "danger")
    return render_template("login.html", title="Sign In", form=form)


@auth_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    flash(f"{current_user.username} Logged Out", "success")
    logout_user()
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/account_settings")
@login_required
def account_settings():
    return render_template("account_settings.html")


@auth_blueprint.route("/update_leaderboard_preference", methods=["POST"])
@login_required
def update_leaderboard_preference():
    if "opt_out_leaderboard" in request.form:
        session["opted_out_of_leaderboard"] = True
    else:
        session["opted_out_of_leaderboard"] = False
    flash("Your leaderboard preferences have been updated.", "success")
    return redirect(url_for("auth.account_settings"))


@auth_blueprint.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    user = User.query.get(current_user.user_id)
    if user:
        user_cards = Card.query.join(Deck).filter(Deck.user_id == user.user_id).all()
        for card in user_cards:
            ReviewOutcome.query.filter_by(card_id=card.card_id).delete()

        db.session.delete(user)
        db.session.commit()

        logout_user()
        flash("Your account has been deleted.", "success")
        return redirect(url_for("main.index"))

    flash("Account deletion failed.", "danger")
    return redirect(url_for("auth.account_settings"))
