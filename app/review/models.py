from app import db
from datetime import datetime
from uuid import uuid4


class ReviewOutcome(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey("card.card_id"), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(36), nullable=False, default=lambda: str(uuid4()))
