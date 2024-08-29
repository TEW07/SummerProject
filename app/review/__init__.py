from flask import Blueprint

review_blueprint = Blueprint("review", __name__, template_folder="templates")

from . import routes
