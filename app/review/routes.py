from flask import render_template, redirect, url_for, flash, abort, request, session
from flask_login import current_user, login_required
from app import db
from app.decks.models import Deck, Card
from . import review_blueprint

@review_blueprint.route('/start_review/<int:deck_id>', methods=['GET'])
@login_required
def start_review(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.user_id:
        abort(403)
    session['deck_id'] = deck_id
    session['card_ids'] = [card.card_id for card in deck.cards]
    session['current_card_index'] = 0
    return redirect(url_for('review.show_card'))

@review_blueprint.route('/show_card')
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
    correct = request.form.get('correct') == 'true'
    card = Card.query.get_or_404(card_id)

    # For now, just process whether the answer was correct or not
    # Logic for updating review status, etc., can be added here

    session['current_card_index'] += 1
    return redirect(url_for('review.show_card'))

@review_blueprint.route('/review_summary')
@login_required
def review_summary():
    return render_template('review_summary.html')


@review_blueprint.route('/review')
@login_required
def review():
    user_decks = Deck.query.filter_by(user_id=current_user.user_id).all()
    return render_template('review.html', decks=user_decks)


