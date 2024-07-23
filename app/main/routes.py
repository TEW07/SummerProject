from flask import render_template, flash
from . import main_blueprint
from app.decks.models import Deck, Card
from app.auth.models import LoginEvent
from datetime import datetime, timedelta
from flask_login import current_user, login_required


@main_blueprint.route('/')
def index():
    return render_template('home.html')


@main_blueprint.route('/dashboard')
@login_required
def dashboard():
    user_decks = Deck.query.filter_by(user_id=current_user.user_id).all()
    due_reviews = []

    for deck in user_decks:
        due_count = Card.query.filter(
            Card.deck_id == deck.deck_id,
            Card.next_review_date <= datetime.utcnow()
        ).count()
        if due_count > 0:
            due_reviews.append({
                'deck_id': deck.deck_id,
                'name': deck.name,
                'due_count': due_count
            })
            flash(f'{due_count} cards due for review in {deck.name}', 'warning')

    # Calculate the current streak
    login_events = LoginEvent.query.filter_by(user_id=current_user.user_id).order_by(LoginEvent.timestamp.desc()).all()
    streak = 0
    today = datetime.utcnow().date()
    expected_date = today

    login_dates = {event.timestamp.date() for event in login_events}

    while expected_date in login_dates:
        streak += 1
        expected_date -= timedelta(days=1)

    user_info = {
        'username': current_user.username,
        'login_count': current_user.get_login_count(current_user.user_id),
        'last_login_at': current_user.get_latest_login(current_user.user_id),
        'current_streak': streak  # Add the current streak to user_info
    }

    return render_template('dashboard.html', due_reviews=due_reviews, user_info=user_info)








