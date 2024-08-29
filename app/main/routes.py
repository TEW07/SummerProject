from datetime import datetime

import pytz
from flask import flash, render_template, session
from flask_login import current_user, login_required
from pytz import timezone

from app.auth.models import LoginEvent
from app.decks.models import Card, Deck

from . import main_blueprint


@main_blueprint.route("/")
def index():
    return render_template("home.html")


@main_blueprint.route("/dashboard")
@login_required
def dashboard():
    user_decks = Deck.query.filter_by(user_id=current_user.user_id).all()
    due_reviews = []

    for deck in user_decks:
        due_count = Card.query.filter(
            Card.deck_id == deck.deck_id, Card.next_review_date <= datetime.utcnow()
        ).count()
        if due_count > 0:
            due_reviews.append({"deck_id": deck.deck_id, "name": deck.name, "due_count": due_count})
            flash(f"{due_count} cards due for review in {deck.name}", "warning")

    login_events = (
        LoginEvent.query.filter_by(user_id=current_user.user_id)
        .order_by(LoginEvent.timestamp.desc())
        .all()
    )
    previous_login_time = login_events[1].timestamp if len(login_events) > 1 else None

    if previous_login_time:
        bst = timezone("Europe/London")
        previous_login_time = previous_login_time.replace(tzinfo=pytz.utc).astimezone(bst)
        previous_login_time_str = previous_login_time.strftime("%d-%m-%Y %H:%M")
    else:
        previous_login_time_str = "N/A"

    streak = session.get("streak", 1)

    user_info = {
        "username": current_user.username,
        "login_count": current_user.get_login_count(current_user.user_id),
        "last_login_at": previous_login_time_str,
        "current_streak": streak,
    }

    return render_template("dashboard.html", due_reviews=due_reviews, user_info=user_info)
