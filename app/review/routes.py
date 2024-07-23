from flask import render_template, redirect, abort, url_for, flash, request, session
from flask_login import current_user, login_required
from app.decks.models import Deck, Card
from app import db
from app.review.models import ReviewOutcome
import uuid
from datetime import datetime, timedelta
from . import review_blueprint


@review_blueprint.route('/start_review/<int:deck_id>', methods=['GET'])
@login_required
def start_review(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.user_id:
        abort(403)

    # Set the review start date if not already set
    if not deck.review_start_date:
        deck.review_start_date = datetime.utcnow()
        db.session.commit()

    session['deck_id'] = deck_id
    session['card_ids'] = [card.card_id for card in deck.cards if card.next_review_date and card.next_review_date <= datetime.utcnow()]
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
    deck_id = session.get('deck_id')
    deck = Deck.query.get(deck_id)

    review_outcome = ReviewOutcome(
        user_id=current_user.user_id,
        card_id=card.card_id,
        correct=correct,
        session_id=session_id
    )
    db.session.add(review_outcome)
    db.session.commit()

    schedule_review(card, correct, deck)
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


REVIEW_SCHEDULE = {
        1: [1, 2],
        2: [1, 3],
        3: [1, 2],
        4: [1, 4],
        5: [1, 2],
        6: [1, 3],
        7: [1, 2],
        8: [1, 2],
        9: [1, 3],
        10: [1, 2, 5],
        11: [1, 4],
        12: [1, 2],
        13: [1, 3],
        14: [1, 2],
    }


def schedule_review(card, success, deck):
    if success:
        if card.box == 5:
            # Card is learned, no need for further review
            card.next_review_date = None
        else:
            card.box += 1
    else:
        card.box = 1

    if card.next_review_date is not None:
        today = datetime.utcnow().date()
        current_cycle_day = ((today - deck.review_start_date.date()).days % 14) + 1
        for offset in range(1, 15):
            next_cycle_day = ((current_cycle_day + offset - 1) % 14) + 1
            if card.box in REVIEW_SCHEDULE[next_cycle_day]:
                card.next_review_date = today + timedelta(days=offset)
                break

        card.next_review_date = datetime.combine(card.next_review_date, datetime.min.time())

    db.session.commit()




def check_due_cards():
    now = datetime.utcnow()
    due_cards = Card.query.filter(Card.next_review_date <= now).all()
    for card in due_cards:
        # Logic to notify user or mark cards as due for review
        pass



