import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecretkey')
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'app', 'data', 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def add_target_column():
    with app.app_context():
        if not os.path.exists(database_path):
            print(f"Database file not found at {database_path}. Creating database.")
            db.create_all()

        with db.engine.connect() as connection:
            connection.execute(text("ALTER TABLE achievement ADD COLUMN target INTEGER DEFAULT 0;"))
            print("Target column added successfully.")


if __name__ == "__main__":
    add_target_column()


