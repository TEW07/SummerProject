from datetime import datetime, timedelta
from app import app, db
from app.auth.models import LoginEvent, User


def generate_pretend_logins(user_id, start_date, num_days):
    """
    Generate pretend logins for a user.

    :param user_id: ID of the user
    :param start_date: The starting date for generating logins
    :param num_days: Number of days to generate logins for
    """
    for i in range(num_days):
        login_date = start_date + timedelta(days=i)
        # Set the timestamp to a different time of the day to ensure uniqueness
        login_timestamp = login_date + timedelta(hours=i % 24, minutes=i % 60)
        login_event = LoginEvent(user_id=user_id, timestamp=login_timestamp)
        db.session.add(login_event)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        user = User.query.filter_by(username='Twotto7').first()
        if user:
            # Clear existing login events for the user
            LoginEvent.query.filter_by(user_id=user.user_id).delete()
            db.session.commit()

            # Generate pretend logins
            generate_pretend_logins(user.user_id, datetime(2024, 7, 14), 10)
            print("Pretend logins generated successfully.")