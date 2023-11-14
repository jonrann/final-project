from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models import user as user_module
from flask_app.models import program as program_module
from flask_app.models import week as week_module
from flask_app.models import day as day_module
from flask_app.models import workout as workout_module
from flask_app import app

@app.route('/create/workout/<int:program_id>', methods=['POST'])
def create_workout(program_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))
    
    # Retrieve data from form, hidden input includes day_id
    workout_data = dict(request.form)
    print(workout_data)

    # Create day object
    day = day_module.Day.get_day_by_id(workout_data.get('day_id'))

    # Get workout ID when creating a new workout
    workout_id = workout_module.Workout.create_workout(workout_data)
    # Create workout object from workout id
    workout = workout_module.Workout.get_workout_by_id(workout_id)
    # Add workout to the day's workout list
    day.workouts.append(workout)
    print(day.workouts)

    return redirect(url_for('view_program_page', program_id=program_id))
