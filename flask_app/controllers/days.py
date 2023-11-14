from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models import user as user_module
from flask_app.models import program as program_module
from flask_app.models import week as week_module
from flask_app.models import day as day_module
from flask_app.models import workout as workout_module
from flask_app import app

# ----- RENDER ROUTES -----

# Incomplete
@app.route('/edit/day/<int:day_id>')
def edit_day_page():
    return render_template('')

@app.route('/day/details/<int:day_id>/<int:program_id>')
def view_day_page(day_id, program_id):
    program = program_module.Program.get_by_id(program_id)
    day = day_module.Day.get_day_by_id(day_id)
    workouts = day.get_all_workouts()
    for workout in workouts:
        workout.get_all_exercises()
    return render_template('view_day.html', day=day, workouts=workouts, program=program)


# ----- POST ROUTES -----

@app.route('/create/day/<int:program_id>', methods=['POST'])
def create_day(program_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))
    
    # Retrieve data from form
    # Hidden input already includes week_id
    day_data = dict(request.form)

    # Create week object
    week  = week_module.Week.get_week_by_id(day_data.get('week_id'))

    # Get day ID when creating a new day
    day_id = day_module.Day.create_day(day_data)
    # Create a day object
    day = day_module.Day.get_day_by_id(day_id)
    # Add day to the week's day list
    week.add_day(day)

    return redirect(url_for('view_program_page', program_id=program_id))

@app.route('/delete/day/<int:day_id>/<int:program_id>', methods=['POST'])
def delete_day(day_id, program_id):
    # Ensure user is logged in to delete a day
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))
    
    # Checks if DB rows were affected; returns true if at least 1 row as affected
    if day_module.Day.delete_day(day_id):
        return redirect(url_for('view_program_page', program_id=program_id))
    # Returns false if no rows were affected
    flash('Failed to delete day', 'danger')
    return redirect(url_for('view_program_page', program_id=program_id))