from flask import render_template
from . import auth_blueprint


@auth_blueprint.route('/login')
def login():
    return render_template('login.html')


@auth_blueprint.route('/register')
def register():
    return render_template('register.html')

