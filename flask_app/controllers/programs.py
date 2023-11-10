from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models import user as user_module
from flask_app.models import program as program_module
from flask_app import app

@app.route('/create/program')
def create_program_page():
    return render_template('create_program.html')


@app.route('/create-program', methods=['POST'])
def create_program():

    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))


    # Retrieve data from form
    program_data = dict(request.form)
    # Add user_id into retrieved data
    program_data['user_id'] = user_id
    
    # Associate new program with current logged in user
    # Create user object with user_id
    user = user_module.User.get_one_by_id(user_id)

    #Create program-- inserting returns id of program
    program_id = program_module.Program.create_program(program_data)
    # Create program object
    program = program_module.Program.get_by_id(program_id)
    # Assign program owner with user object
    program.owner = user
    
    # Redirect to dashboard
    flash('Program created', 'success')
    return redirect(url_for('dashboard'))