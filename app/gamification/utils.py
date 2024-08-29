# app/gamification/utils.py
from flask import flash
from app import db
from .models import Achievement, UserAchievement
from app.review.models import ReviewOutcome


def check_achievements(user):
    total_cards_reviewed = (
        db.session.query(ReviewOutcome).filter_by(user_id=user.user_id).count()
    )
    achievements = Achievement.query.all()

    for achievement in achievements:
        if achievement.name.endswith("Cards Reviewed"):
            # Check based on cards reviewed
            if total_cards_reviewed >= int(achievement.target):
                award_achievement(user.user_id, achievement.achievement_id)
        else:
            # Check based on points
            if user.points >= int(achievement.target):
                award_achievement(user.user_id, achievement.achievement_id)


def award_achievement(user_id, achievement_id):
    existing_achievement = UserAchievement.query.filter_by(
        user_id=user_id, achievement_id=achievement_id
    ).first()
    if not existing_achievement:
        new_achievement = UserAchievement(
            user_id=user_id, achievement_id=achievement_id
        )
        db.session.add(new_achievement)
        db.session.commit()
        achievement = Achievement.query.get(achievement_id)
        flash(
            f"Congratulations! You have earned the achievement: {achievement.name}",
            "success",
        )
