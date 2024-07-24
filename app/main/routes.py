from flask import render_template, flash, session
from . import main_blueprint
from app.decks.models import Deck, Card
from app.auth.models import User
from datetime import datetime
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

    user_info = {
        'username': current_user.username,
        'login_count': current_user.get_login_count(current_user.user_id),
        'last_login_at': current_user.get_latest_login(current_user.user_id),
        'current_streak': session.get('streak', 0)  # Retrieve the streak from the session
    }

    return render_template('dashboard.html', due_reviews=due_reviews, user_info=user_info)



@main_blueprint.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.points.desc()).limit(10).all()  # Get top 10 users
    return render_template('leaderboard.html', users=users)









