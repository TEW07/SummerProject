from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_login_count(self, user_id):
        return LoginEvent.query.filter_by(user_id=user_id).count()

    def get_latest_login(self, user_id):
        latest_login_event = LoginEvent.query.filter_by(user_id=user_id).order_by(LoginEvent.timestamp.desc()).first()
        return latest_login_event.timestamp if latest_login_event else None

    def get_cycle_day(self):
        days_since_start = (datetime.utcnow().date() - self.cycle_start_date.date()).days
        return (days_since_start % 14) + 1

    def __repr__(self):
        return f"user('{self.username}', '{self.email}')"


class LoginEvent(db.Model):
    login_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"LoginEvent('{self.user_id}', '{self.timestamp}')"





