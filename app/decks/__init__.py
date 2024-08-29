from flask import Blueprint

decks_blueprint = Blueprint("decks", __name__, template_folder="templates")

from . import routes
