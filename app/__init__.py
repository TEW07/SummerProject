from flask import Flask
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate a random 32-character hexadecimal string as secret key

from .views import main
app.register_blueprint(main)


