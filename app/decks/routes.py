from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import current_user, login_required
from app import db
from . import decks_blueprint
from .forms import CreateDeckForm, AddCardForm, EditCardForm
from .models import Deck, Card
from app.auth.models import User
from datetime import datetime
from app.review.models import ReviewOutcome


@decks_blueprint.route('/create_deck', methods=['GET', 'POST'])
@login_required
def create_deck():
    form = CreateDeckForm()
    if form.validate_on_submit():
        deck = Deck(name=form.name.data, user_id=current_user.user_id)
        db.session.add(deck)
        db.session.commit()
        flash('Your deck has been created!', 'success')
        return redirect(url_for('decks.decks'))
    return render_template('create_deck.html', form=form)


@decks_blueprint.route('/decks')
@login_required
def decks():
    user_decks = Deck.query.filter_by(user_id=current_user.user_id).all()
    deck_data = []

    for deck in user_decks:
        card_count = Card.query.filter_by(deck_id=deck.deck_id).count()
        due_count = Card.query.filter(Card.deck_id == deck.deck_id,
                                      Card.next_review_date <= datetime.utcnow()).count()

        # Step 1: Query for the earliest next_review_date for the cards in the deck
        next_review = db.session.query(Card.next_review_date).filter(
            Card.deck_id == deck.deck_id
        ).order_by(Card.next_review_date.asc()).first()

        # Step 2: Set next_review_date based on the query result
        if next_review:
            # Check if the next_review_date is in the past
            if next_review.next_review_date.date() < datetime.utcnow().date():
                next_review_date = datetime.utcnow().strftime('%Y-%m-%d')
            else:
                next_review_date = next_review.next_review_date.strftime('%Y-%m-%d')
        else:
            next_review_date = 'N/A'

        # Get the last review date
        last_review = db.session.query(ReviewOutcome.timestamp).join(Card,
                                                                     Card.card_id == ReviewOutcome.card_id).filter(
            Card.deck_id == deck.deck_id,
            ReviewOutcome.user_id == current_user.user_id
        ).order_by(ReviewOutcome.timestamp.desc()).first()
        last_review_date = last_review.timestamp.strftime('%Y-%m-%d') if last_review else 'N/A'

        deck_data.append({
            'deck_id': deck.deck_id,
            'name': deck.name,
            'cards': card_count,
            'due_for_review': due_count,
            'shared': deck.shared,
            'next_review_date': next_review_date,
            'last_review_date': last_review_date
        })

    return render_template('decks.html', decks=deck_data)







@decks_blueprint.route('/view_deck/<int:deck_id>')
@login_required
def view_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    is_owner = deck.user_id == current_user.user_id
    if not deck.shared and not is_owner:
        abort(403)  # Forbidden access if the deck is not shared and not owned by the current user

    cards = Card.query.filter_by(deck_id=deck.deck_id).all()
    return render_template('view_deck.html', deck=deck, cards=cards)


@decks_blueprint.route('/add_card', methods=['GET', 'POST'])
@login_required
def add_card():
    user_decks = Deck.query.filter_by(user_id=current_user.user_id).all()
    form = AddCardForm()
    form.deck.choices = [(deck.deck_id, deck.name) for deck in user_decks]  # Populate form dropdown

    if form.validate_on_submit():
        card = Card(
            front=form.front.data,
            back=form.back.data,
            deck_id=form.deck.data,
            next_review_date=datetime.utcnow(),  # Schedule for immediate review
            box=1  # New cards start in box 1
        )
        db.session.add(card)
        db.session.commit()
        flash('Card has been added!', 'success')
        return redirect(url_for('decks.decks'))

    return render_template('add_card.html', title='Add Card', form=form)


@decks_blueprint.route('/edit_card/<int:card_id>', methods=['GET', 'POST'])
@login_required
def edit_card(card_id):
    card = Card.query.get_or_404(card_id)
    if card.deck.user_id != current_user.user_id:
        abort(403)
    form = EditCardForm()

    if form.validate_on_submit():
        card.front = form.front.data
        card.back = form.back.data
        db.session.commit()
        flash('Your card has been updated!', 'success')
        return redirect(url_for('decks.view_deck', deck_id=card.deck_id))
    elif request.method == 'GET':
        form.front.data = card.front
        form.back.data = card.back

    return render_template('edit_card.html', title='Edit Card', form=form, card=card)


@decks_blueprint.route('/delete_card/<int:card_id>', methods=['POST', 'GET'])
@login_required
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    if card.deck.user_id != current_user.user_id:
        abort(403)
    db.session.delete(card)
    db.session.commit()
    flash('Card has been deleted!', 'success')
    return redirect(url_for('decks.view_deck', deck_id=card.deck_id))


@decks_blueprint.route('/delete_deck/<int:deck_id>', methods=['POST', 'GET'])
@login_required
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.user_id:
        abort(403)

    Card.query.filter_by(deck_id=deck_id).delete()

    db.session.delete(deck)
    db.session.commit()
    flash('Deck has been deleted!', 'success')
    return redirect(url_for('decks.decks'))


@decks_blueprint.route('/share_deck/<int:deck_id>', methods=['POST', 'GET'])
@login_required
def share_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.user_id:
        abort(403)
    deck.shared = not deck.shared
    db.session.commit()
    flash(f'Deck {"shared" if deck.shared else "unshared"} successfully!', 'success')
    return redirect(url_for('decks.decks'))


@decks_blueprint.route('/public_decks')
@login_required
def public_decks():
    shared_decks = Deck.query.filter_by(shared=True).all()
    deck_data = []

    for deck in shared_decks:
        card_count = Card.query.filter_by(deck_id=deck.deck_id).count()
        creator = User.query.get(deck.user_id).username  # Fetch the username of the deck creator
        deck_data.append({
            'deck_id': deck.deck_id,
            'name': deck.name,
            'cards': card_count,
            'creator': creator  # Add the creator's username to the deck data
        })

    return render_template('public_decks.html', decks=deck_data)


@decks_blueprint.route('/clone_deck/<int:deck_id>', methods=['POST', 'GET'])
@login_required
def clone_deck(deck_id):
    original_deck = Deck.query.get_or_404(deck_id)
    new_deck = Deck(name='CLONE: ' + original_deck.name, user_id=current_user.user_id, review_start_date=datetime.utcnow())
    db.session.add(new_deck)
    db.session.commit()

    original_cards = Card.query.filter_by(deck_id=deck_id).all()
    for card in original_cards:
        new_card = Card(front=card.front, back=card.back, deck_id=new_deck.deck_id, box=1)
        new_card.next_review_date = datetime.utcnow()  # Schedule for review immediately
        db.session.add(new_card)

    db.session.commit()
    flash('Deck has been cloned successfully!', 'success')
    return redirect(url_for('decks.decks'))





