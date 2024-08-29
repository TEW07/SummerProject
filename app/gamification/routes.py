from flask import render_template, session
from flask_login import current_user, login_required

from app import db
from app.auth.models import User
from app.review.models import ReviewOutcome

from . import gamification_blueprint
from .models import Achievement, UserAchievement


@gamification_blueprint.route("/leaderboard")
def leaderboard():
    if session.get("opted_out_of_leaderboard"):
        users = (
            User.query.filter(User.user_id != current_user.user_id)
            .order_by(User.points.desc())
            .all()
        )
    else:
        users = User.query.order_by(User.points.desc()).all()
    return render_template("leaderboard.html", users=users)


@gamification_blueprint.route("/user_achievements")
@login_required
def user_achievements():
    user_achievements = UserAchievement.query.filter_by(user_id=current_user.user_id).all()
    all_achievements = Achievement.query.all()
    user_achievements_dict = {ua.achievement_id: ua for ua in user_achievements}

    achievements_with_progress = [
        {
            "achievement": ua,
            "progress": calculate_progress(ua),
            "formatted_date": ua.date_earned.strftime("%d/%m/%Y %H:%M"),
        }
        for ua in user_achievements
    ]

    all_achievements_with_progress = [
        {"achievement": achievement, "progress": calculate_progress_all(achievement)}
        for achievement in all_achievements
        if achievement.achievement_id not in user_achievements_dict
    ]

    return render_template(
        "user_achievements.html",
        achievements_with_progress=achievements_with_progress,
        all_achievements_with_progress=all_achievements_with_progress,
        user_achievements=user_achievements_dict,
    )


def calculate_progress(user_achievement):
    total_unique_cards_reviewed = (
        db.session.query(ReviewOutcome.card_id)
        .filter_by(user_id=current_user.user_id)
        .distinct()
        .count()
    )

    if "Cards Reviewed" in user_achievement.achievement.name:
        if user_achievement.achievement.target > 0:
            progress = (
                total_unique_cards_reviewed / int(user_achievement.achievement.target)
            ) * 100
            return min(progress, 100)
    else:
        if user_achievement.achievement.target > 0:
            progress = (current_user.points / user_achievement.achievement.target) * 100
            return min(progress, 100)

    return 0


def calculate_progress_all(achievement):
    total_unique_cards_reviewed = (
        db.session.query(ReviewOutcome.card_id)
        .filter_by(user_id=current_user.user_id)
        .distinct()
        .count()
    )

    if "Cards Reviewed" in achievement.name:
        if achievement.target > 0:
            return min((total_unique_cards_reviewed / int(achievement.target)) * 100, 100)
    else:
        if achievement.target > 0:
            return min((current_user.points / achievement.target) * 100, 100)

    return 0
