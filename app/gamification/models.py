from app import db
from datetime import datetime


class Achievement(db.Model):
    achievement_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    badge_image = db.Column(db.String(255), nullable=False)
    target = db.Column(db.Integer, nullable=False, default=0)
    users = db.relationship(
        "UserAchievement", back_populates="achievement", cascade="all, delete-orphan"
    )


class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    achievement_id = db.Column(
        db.Integer, db.ForeignKey("achievement.achievement_id"), nullable=False
    )
    date_earned = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship("User", back_populates="achievements")
    achievement = db.relationship("Achievement", back_populates="users")
