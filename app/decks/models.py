from app import db
from datetime import datetime


class Deck(db.Model):
    deck_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return f"Deck('{self.name}', '{self.user_id}')"


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(255), nullable=False)
    back = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    next_review_date = db.Column(db.DateTime, default=datetime.utcnow)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.deck_id'), nullable=False)

    def __repr__(self):
        return f"Card('{self.front}', '{self.back}')"
