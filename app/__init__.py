# app/__init__.py
from flask import Flask

app = Flask(__name__)

# Register Blueprints
from .views import main
app.register_blueprint(main)

