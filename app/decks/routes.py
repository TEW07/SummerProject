from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from . import decks_blueprint
from .forms import CreateDeckForm, AddCardForm
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
    # Query to get all decks for the current user
    user_decks = Deck.query.filter_by(user_id=current_user.user_id).all()
    return render_template('decks.html', decks=user_decks)


@decks_blueprint.route('/add_card', methods=['GET', 'POST'])
@login_required
def add_card():
    form = AddCardForm()
    if form.validate_on_submit():
        card = Card(front=form.front.data, back=form.back.data, deck_id=form.deck_id.data)
        db.session.add(card)
        db.session.commit()
        flash('Card added successfully!', 'success')
        return redirect(url_for('decks.decks', deck_id=form.deck_id.data))
    return render_template('add_card.html', title='Add Card', form=form)
