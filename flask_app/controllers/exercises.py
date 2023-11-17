from flask import render_template, request, redirect, session, flash, url_for
from flask_app.models import user as user_module
from flask_app.models import program as program_module
from flask_app.models import week as week_module
from flask_app.models import day as day_module
from flask_app.models import workout as workout_module
from flask_app.models import exercise as exercise_module
from flask_app import app

# ----- RENDER ROUTES ------

@app.route('/create/exercise/<int:workout_id>/<int:day_id>/<int:program_id>')
def create_exercise_page(workout_id, day_id, program_id):
    if 'user_id' not in session:
        flash('Must log into view this page', 'danger')
        return redirect(url_for('login_page'))
    workout = workout_module.Workout.get_workout_by_id(workout_id)
    program = program_module.Program.get_by_id(program_id)
    day = day_module.Day.get_day_by_id(day_id)
    return render_template('create_exercise.html', workout=workout, day_id=day_id, program_id=program_id, program=program, day=day)

# ----- POST ROUTES ------
@app.route('/create-exercise/<int:workout_id>/<int:day_id>/<int:program_id>', methods=['POST'])
def create_exercise(workout_id, day_id, program_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))
    
    program = program_module.Program.get_by_id(program_id)
    day = day_module.Day.get_day_by_id(day_id)
    
    # Retrieve Exercise Data
    exercise_data = dict(request.form)
    print(exercise_data)
    # Create object and save exercise to DB
    exercise_id = exercise_module.Exercise.create_exercise(exercise_data)
    exercise = exercise_module.Exercise.get_exercise_by_id(exercise_id)

    # Get Workout object by id
    workout = workout_module.Workout.get_workout_by_id(workout_id)
    # Associate exercise with workout object
    workout.exercises.append(exercise)

    return redirect(url_for('view_day_page', day=day, program=program, day_id=day_id, program_id=program_id))

@app.route('/update-exercise/<int:workout_id>/<int:day_id>/<int:program_id>', methods=['POST'])
def update_exercise(workout_id, day_id, program_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Log in to create a program', 'danger')
        return redirect(url_for('login_page'))
    
    new_exercise_data = dict(request.form)
    
    if exercise_module.Exercise.update_exercise(new_exercise_data):
        flash('Updated exercise', 'success')
        return redirect(url_for('view_day_page', day_id=day_id, program_id=program_id, workout_id=workout_id))
    flash('Failed to update', 'danger')
    return redirect(url_for('view_day_page', day_id=day_id, program_id=program_id, workout_id=workout_id))
