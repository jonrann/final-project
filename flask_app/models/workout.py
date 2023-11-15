from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import exercise as exercise_module

class Workout:
    def __init__(self, data) -> None:
        self.id = data.get('id')
        self.day_id = data.get('day_id')
        self.title = data.get('title', 'Default Title')
        self.warmup = data.get('warmup', 'No warm-up')
        self.cooldown = data.get('cooldown', 'No cooldown')
        self.exercises = []
        self.day = None

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def get_all_exercises(self):
        self.exercises = exercise_module.Exercise.get_all_by_workout_id(self.id)

    @classmethod
    def create_workout(cls, data):
        query = """
            INSERT INTO workouts (
                day_id,
                title,
                warmup,
                cooldown
            )
            VALUES (
                %(day_id)s,
                %(title)s,
                %(warmup)s,
                %(cooldown)s
            )
        """
        return connectToMySQL('workout_tracker_schema').query_db(query, data)
    
    @classmethod
    def get_workout_by_id(cls, workout_id):
        query = "SELECT * FROM workouts WHERE id = %(id)s;"

        data = {
            'id': workout_id
        }
        result = connectToMySQL('workout_tracker_schema').query_db(query, data)

        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_all_by_day_id(cls, day_id):
        query = "SELECT * FROM workouts WHERE day_id = %(day_id)s;"
        data = {
            'day_id': day_id
        }

        results = connectToMySQL('workout_tracker_schema').query_db(query, data)

        workouts = []

        for row in results:
            workouts.append(cls(row))
        return workouts
    
    @classmethod
    def update_workout(cls, data):
        query = """
            UPDATE workouts
            SET warmup = %(warmup)s,
                cooldown = %(cooldown)s
            WHERE id = %(id)s;
        """
        return connectToMySQL('workout_tracker_schema').query_db(query, data)
    
    @classmethod
    def delete_workout(cls, workout_id):
        query = "DELETE FROM workouts WHERE id = %(id)s;"

        data = {
            'id': workout_id
        }

        return connectToMySQL('workout_tracker_schema').query_db(query, data)