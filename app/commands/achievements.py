from flask.cli import with_appcontext
import click
from app import db
from app.gamification.models import Achievement


@click.command(name="delete_achievements")
@with_appcontext
def delete_achievements():
    achievements = Achievement.query.all()
    for achievement in achievements:
        db.session.delete(achievement)
    db.session.commit()
    print("All achievements deleted successfully!")


@click.command(name="add_achievements")
@with_appcontext
def add_achievements():
    achievements = [
        Achievement(
            name="10 Cards Reviewed",
            description="Review 10 Different Cards",
            points=0,
            badge_image="badges/10_cards_badge.png",
            target="10",
        ),
        Achievement(
            name="50 Cards Reviewed",
            description="Review 50 Different Cards",
            points=0,
            badge_image="badges/50_cards_badge.png",
            target="50",
        ),
        Achievement(
            name="100 Cards Reviewed",
            description="Review 100 Different Cards",
            points=0,
            badge_image="badges/100_cards_badge.png",
            target=100,
        ),
        Achievement(
            name="100 Points",
            description="Reach 100 Points",
            points=0,
            badge_image="badges/100_points_badge.png",
            target=100,
        ),
        Achievement(
            name="500 Points",
            description="Reach 500 Points",
            points=0,
            badge_image="badges/500_points_badge.png",
            target=500,
        ),
        Achievement(
            name="1000 Points",
            description="Reach 1000 Points",
            points=0,
            badge_image="badges/1000_points_badge.png",
            target=1000,
        ),
    ]

    for achievement in achievements:
        existing_achievement = Achievement.query.filter_by(
            name=achievement.name
        ).first()
        if not existing_achievement:
            db.session.add(achievement)

    db.session.commit()
    print("Achievements added successfully!")
