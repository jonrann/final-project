from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models import user as user_module
from flask_app.models import program as program_module
from flask_app.models import week as week_module
from flask_app import app



# ----- POST ROUTES -----

@app.route('/create-week/<int:program_id>', methods=['POST'])
def create_week(program_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))
    
    # Retrieve data from form
    week_data = dict(request.form)
    # Add program_id into retrieved data
    week_data['program_id'] = program_id

    # Create program object
    program = program_module.Program.get_by_id(program_id)

    # Get week ID when creating a new week
    week_id = week_module.Week.create_week(week_data)
    # Create week object by using week id
    week = week_module.Week.get_week_by_id(week_id)

    # Add week to program object's attribute: weeks
    program.add_week(week)

    return redirect(url_for('view_program_page', program=program, program_id=program_id))

@app.route('/delete-week/<int:week_id>/<int:program_id>', methods=['POST'])
def delete_week(week_id, program_id):
    # Ensure user is logged in to delete a week
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))
    
    # If row is affected in DB, return True
    if week_module.Week.delete_week(week_id):
        return redirect(url_for('view_program_page', program_id=program_id))
    # Returns false if no rows were affected
    flash('Failed to delete week', 'danger')
    return redirect(url_for('view_program_page', program_id=program_id))
