from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models import user as user_module
from flask_app.models import program as program_module
from flask_app.models import week as week_module
from flask_app.models import day as day_module

from flask_app import app

@app.route('/create/program')
def create_program_page():
    return render_template('create_program.html')


@app.route('/program/<int:program_id>')
def view_program_page(program_id):
    # Get one specific program
    program = program_module.Program.get_by_id(program_id)

    # Get all the weeks associated with that program
    program.get_all_weeks()

    # Get all days associated with each week and calculate next day number
    for week in program.weeks:
        week.get_all_days()
        for day in week.days:
            day.get_all_workouts()

        # Calculate the next day number for each week, ensuring it doesn't exceed 7
        week.next_day_number = min(len(week.days) + 1, 7)

    # Calculate the next week number, ensuring it doesn't exceed 8
    next_week_number = min(len(program.weeks) + 1, 8)

    return render_template('view_program.html', program=program, next_week_number=next_week_number)



@app.route('/edit-program/<int:program_id>')
def view_edit_program_page(program_id):
    # Get content for one program
    program = program_module.Program.get_by_id(program_id)
    return render_template('edit_program.html', program=program)


# ----- POST ROUTES -----

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

@app.route('/delete/program/<int:program_id>', methods=['POST'])
def delete_program(program_id):
    # Make sure user is logged in to delete a program
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))

    # Run query, delete program; check if successful else flash
    if program_module.Program.delete_program(program_id):
        flash('Program successfully deleted', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Failed to delete program', 'danger')
        return redirect(url_for('view_program_page', program_id=program_id))

@app.route('/edit/program/<int:program_id>', methods=['POST'])
def update_program(program_id):
    # Make sure user is logged in to delete a program
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))
    
    # Retrieve updated data from form
    new_program_data = dict(request.form)
    # Take data and run through in query
    if program_module.Program.update_program(new_program_data):
        # Redirect to program details page
        flash('Program successfully updated', 'success')
        return redirect(url_for('view_program_page', program_id=program_id))
    flash('Failed to update program', 'danger')
    return redirect(url_for('view_program_page', program_id=program_id))