from flask import render_template, url_for, flash, redirect
from app.auth import auth_blueprint
from app.auth.forms import RegistrationForm
from .models import User
from app import db

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth_blueprint.route('/login')
def login():
    return render_template('login.html', title='Login')

