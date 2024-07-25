from flask import Blueprint

gamification_blueprint = Blueprint('gamification', __name__)

from . import routes
