from flask import Blueprint, render_template, redirect, abort, url_for, flash, request, session
from flask_login import current_user, login_required
from app.decks.models import Deck, Card
from app import db
from app.review.models import ReviewOutcome
import uuid

review_blueprint = Blueprint('review', __name__, template_folder='templates')


@review_blueprint.route('/start_review/<int:deck_id>', methods=['GET'])
@login_required
def start_review(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.user_id:
        abort(403)
    session['deck_id'] = deck_id
    session['card_ids'] = [card.card_id for card in deck.cards]
    session['current_card_index'] = 0
    session['session_id'] = str(uuid.uuid4())
    return redirect(url_for('review.show_card'))


@review_blueprint.route('/show_card', methods=['GET'])
@login_required
def show_card():
    card_ids = session.get('card_ids')
    current_card_index = session.get('current_card_index', 0)

    if current_card_index >= len(card_ids):
        return redirect(url_for('review.review_summary'))

    card = Card.query.get(card_ids[current_card_index])
    return render_template('show_card.html', card=card)


@review_blueprint.route('/process_review/<int:card_id>', methods=['POST'])
@login_required
def process_review(card_id):
    correct = request.form.get('correct') == '1'
    card = Card.query.get_or_404(card_id)
    session_id = session.get('session_id')

    review_outcome = ReviewOutcome(
        user_id=current_user.user_id,
        card_id=card.card_id,
        correct=correct,
        session_id=session_id
    )
    db.session.add(review_outcome)
    db.session.commit()

    session['current_card_index'] += 1
    return redirect(url_for('review.show_card'))


@review_blueprint.route('/review_summary')
@login_required
def review_summary():
    session_id = session.get('session_id')
    if not session_id:
        flash("No review session found. Please start a review session first.", 'warning')
        return redirect(url_for('decks.decks'))

    review_outcomes = ReviewOutcome.query.filter_by(session_id=session_id).all()
    if not review_outcomes:
        flash("No review outcomes to display. Please complete a review session first.", 'info')
        return redirect(url_for('decks.decks'))

    correct_count = sum(1 for outcome in review_outcomes if outcome.correct)
    incorrect_count = len(review_outcomes) - correct_count

    return render_template('review_summary.html', correct_count=correct_count, incorrect_count=incorrect_count,
                           total=len(review_outcomes))




