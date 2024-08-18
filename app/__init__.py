import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import secrets
import pytz
from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://summerprojectpsql_user:37pCeCeAN3b0BjGUEOtdGH1PocpE9Ua5@dpg-cqvlnt8gph6c738uits0-a.frankfurt-postgres.render.com/summerprojectpsql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Put this in your configuration file or where you initialize your app
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
uk_timezone = pytz.timezone('Europe/London')

from .main.routes import main_blueprint
from .auth.routes import auth_blueprint
from .decks.routes import decks_blueprint
from .review.routes import review_blueprint
from app.auth.models import *
from .gamification.routes import gamification_blueprint  # Add this line

app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(decks_blueprint)
app.register_blueprint(review_blueprint)
app.register_blueprint(gamification_blueprint)  # Add this line

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


from app.auth.models import User
from app.decks.models import Deck, Card
from app.gamification.models import Achievement, UserAchievement

from app.commands.achievements import add_achievements, delete_achievements
app.cli.add_command(add_achievements)
app.cli.add_command(delete_achievements)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, LoginEvent=LoginEvent, Card=Card, Deck=Deck)

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template("429.html"), 429


@app.template_filter('to_uk_time')
def to_uk_time(date):
    """Convert a datetime object to UK time and format it."""
    if date.tzinfo is None:  # If the datetime is naive, assume it's in UTC
        date = pytz.utc.localize(date)
    uk_date = date.astimezone(uk_timezone)
    return uk_date.strftime('%d/%m/%Y %H:%M')

app.jinja_env.filters['to_uk_time'] = to_uk_time