# app/auth/models.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    points = db.Column(db.Integer, default=0)  # Add points column
    achievements = db.relationship(
        "UserAchievement", back_populates="user", cascade="all, delete-orphan"
    )
    show_on_leaderboard = db.Column(
        db.Boolean, default=True
    )  # Ensure this column is present

    # Relationship to LoginEvent with cascade delete
    login_events = db.relationship(
        "LoginEvent", backref="user", cascade="all, delete-orphan", lazy=True
    )
    decks = db.relationship(
        "Deck", backref="user", cascade="all, delete-orphan", lazy=True
    )

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_login_count(self, user_id):
        return LoginEvent.query.filter_by(user_id=user_id).count()

    def get_latest_login(self, user_id):
        latest_login_event = (
            LoginEvent.query.filter_by(user_id=user_id)
            .order_by(LoginEvent.timestamp.desc())
            .first()
        )
        return latest_login_event.timestamp if latest_login_event else None

    def __repr__(self):
        return f"user('{self.username}', '{self.email}')"


class LoginEvent(db.Model):
    login_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"LoginEvent('{self.user_id}', '{self.timestamp}')"
