from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from .models import Achievement, UserAchievement
from app.auth.models import User
from . import gamification_blueprint

@gamification_blueprint.route('/leaderboard')
@login_required
def leaderboard():
    users = User.query.order_by(User.points.desc()).limit(10).all()  # Get top 10 users
    return render_template('leaderboard.html', users=users)

def award_achievement(user_id, achievement_id):
    existing_achievement = UserAchievement.query.filter_by(user_id=user_id, achievement_id=achievement_id).first()
    if not existing_achievement:
        new_achievement = UserAchievement(user_id=user_id, achievement_id=achievement_id)
        db.session.add(new_achievement)
        db.session.commit()
        achievement = Achievement.query.get(achievement_id)
        flash(f'Congratulations! You have earned the achievement: {achievement.name}', 'success')

# Example function to award an achievement based on some criteria
def check_achievements(user):
    achievements = Achievement.query.all()
    for achievement in achievements:
        if user.points >= achievement.target:
            award_achievement(user.user_id, achievement.achievement_id)

@gamification_blueprint.route('/user_achievements')
@login_required
def user_achievements():
    user_achievements = UserAchievement.query.filter_by(user_id=current_user.user_id).all()
    all_achievements = Achievement.query.all()
    user_achievements_dict = {ua.achievement_id: ua for ua in user_achievements}

    achievements_with_progress = [
        {
            'achievement': ua,
            'progress': calculate_progress(ua)
        } for ua in user_achievements
    ]

    all_achievements_with_progress = [
        {
            'achievement': achievement,
            'progress': calculate_progress_all(achievement)
        } for achievement in all_achievements if achievement.achievement_id not in user_achievements_dict
    ]

    return render_template(
        'user_achievements.html',
        achievements_with_progress=achievements_with_progress,
        all_achievements_with_progress=all_achievements_with_progress,
        user_achievements=user_achievements_dict
    )

def calculate_progress(user_achievement):
    if user_achievement.achievement.target > 0:
        progress = (current_user.points / user_achievement.achievement.target) * 100
        return min(progress, 100)
    return 0

def calculate_progress_all(achievement):
    if achievement.target > 0:
        return (current_user.points / achievement.target) * 100
    return 0










