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


@click.command(name='update_targets')
@with_appcontext
def update_targets():
    # Define the new achievements with their targets
    achievements_with_targets = [
        {'name': '100 Points Achieved', 'target': 100},
        {'name': '500 Points Achieved', 'target': 500},
        {'name': '1000 Points Achieved', 'target': 1000}
    ]

    # Update the existing achievements with the new target values
    for item in achievements_with_targets:
        achievement = Achievement.query.filter_by(name=item['name']).first()
        if achievement:
            achievement.target = item['target']
            db.session.commit()
            print(f"Updated {item['name']} with target {item['target']}.")

    print("Achievements updated successfully!")

@click.command(name='delete_achievements')
@with_appcontext
def delete_achievements():
    achievements = Achievement.query.all()
    for achievement in achievements:
        db.session.delete(achievement)
    db.session.commit()
    print("All achievements deleted successfully!")


