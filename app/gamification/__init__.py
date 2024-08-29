from flask import Blueprint

gamification_blueprint = Blueprint("gamification", __name__, template_folder="templates")

from . import routes
