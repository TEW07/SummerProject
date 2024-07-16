from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import current_user, login_required
from app import db
from . import decks_blueprint
from .forms import CreateDeckForm, AddCardForm, EditCardForm
from .models import Deck, Card


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
        deck_data.append({
            'deck_id': deck.deck_id,
            'name': deck.name,
            'cards': card_count,
            'next_review_date': '',  # Add logic for next review date
            'last_review_date': ''  # Add logic for last review date
        })

    return render_template('decks.html', decks=deck_data)


@decks_blueprint.route('/view_deck/<int:deck_id>')
@login_required
def view_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.user_id:
        abort(403)  # Forbidden access
    cards = Card.query.filter_by(deck_id=deck.deck_id).all()
    return render_template('view_deck.html', deck=deck, cards=cards)


@decks_blueprint.route('/add_card', methods=['GET', 'POST'])
@login_required
def add_card():
    user_decks = Deck.query.filter_by(user_id=current_user.user_id).all()
    form = AddCardForm()
    form.deck.choices = [(deck.deck_id, deck.name) for deck in user_decks]

    if form.validate_on_submit():
        card = Card(
            front=form.front.data,
            back=form.back.data,
            deck_id=form.deck.data,
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
        deck_data.append({
            'deck_id': deck.deck_id,
            'name': deck.name,
            'cards': card_count,
            'next_review_date': '',  # Add logic for next review date
            'last_review_date': ''   # Add logic for last review date
        })

    return render_template('public_decks.html', decks=deck_data)


