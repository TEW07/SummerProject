# app/decks/models.py
from app import db
from datetime import datetime


class Deck(db.Model):
    deck_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shared = db.Column(db.Boolean, default=False)
    review_start_date = db.Column(db.DateTime, nullable=True)

    # Relationship to Card with cascade delete
    cards = db.relationship('Card', backref='deck', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"Deck('{self.name}', '{self.user_id}')"


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(255), nullable=False)
    back = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    next_review_date = db.Column(db.DateTime, nullable=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.deck_id'), nullable=False)
    box = db.Column(db.Integer, default=1)  # New field for Leitner system

    def __repr__(self):
        return f"Card('{self.front}', '{self.back}')"

