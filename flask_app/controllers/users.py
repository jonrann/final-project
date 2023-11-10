from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models import user as user_module
from flask_app.models import program as program_module
from flask_app import app
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

bcrypt = Bcrypt(app)


# ----- RENDER ROUTES -----

@app.route('/login')
def login_page():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = user_module.User.get_one_by_id(user_id)
        program_list = program_module.Program.get_all_by_user_id(user.id)
        return render_template('dashboard.html', user=user, program_list=program_list)
    flash('Please log in to access dashboard')
    return render_template('register.html')


# ----- POST ROUTES -----


@app.route('/register', methods= ['POST'])
def register():
    user_data = dict(request.form)
    # Check user data
    if user_module.User.validate_user(user_data):
        # If validated, generate hashed password and save user to DB
        hashed_pw = generate_password_hash(user_data['password'])
        user_data['password'] = hashed_pw
        # Save user to DB
        user_id = user_module.User.create_user(user_data)
        if user_id:
            session['user_id'] = user_id
            flash('Register successful', 'register_success')
            return redirect(url_for('dashboard'))
        else:
            flash('Register failed. Try again.', 'register_error')
            return redirect(url_for('login_page'))
    # Return back to login page if user data validation fails
    else:
        return redirect(url_for('login_page'))
    
@app.route('/login', methods=['POST'])
def login():
    user_data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    # Check if email is in DB and create user object if true
    user = user_module.User.get_one_by_email(user_data['email'])

    if user:
        # Check password if it matches hashed password in DB
        if check_password_hash(user.password, user_data['password']):
            session['user_id'] = user.id
            flash('Login successful', 'login_success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect password', 'login_error')
            return redirect(url_for('login_page'))
    else:
        flash('Email not found', 'login_error')
        return redirect(url_for('login_page'))


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login_page'))
