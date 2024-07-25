from flask import current_app
from flask.cli import with_appcontext
import click
from app import db
from app.gamification.models import Achievement

@click.command(name='add_achievements')
@with_appcontext
def add_achievements():
    achievements = [
        Achievement(name='100 Points Achieved', description='Earn 100 points', points=0, badge_image='path/to/100_points_badge.png'),
        Achievement(name='500 Points Achieved', description='Earn 500 points', points=0, badge_image='path/to/500_points_badge.png'),
        Achievement(name='1000 Points Achieved', description='Earn 1000 points', points=0, badge_image='path/to/1000_points_badge.png')
    ]

    for achievement in achievements:
        db.session.add(achievement)

    db.session.commit()
    print("Achievements added successfully!")


@click.command(name='update_achievements')
@with_appcontext
def update_achievements():
    updates = {
        '100 Points Achieved': 'badges/100_points_badge.png',
        '500 Points Achieved': 'badges/500_points_badge.png',
        '1000 Points Achieved': 'badges/1000_points_badge.png'
    }

    for name, path in updates.items():
        achievement = Achievement.query.filter_by(name=name).first()
        if achievement:
            achievement.badge_image = path
            db.session.commit()
            print(f"Updated {name} with new badge path.")


