from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models import user as user_module
from flask_app import app
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

bcrypt = Bcrypt(app)

@app.route('/login')
def login_page():
    return render_template('register.html')

@app.route('/register', methods= ['POST'])
def register():
    user_data = dict(request.form)
    user = user_module.User.create_user(user_data)
    if user:
        return redirect(url_for('login_page'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    return