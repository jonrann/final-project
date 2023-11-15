from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import workout as workout_module

class Day:
    def __init__(self, data) -> None:
        self.id = data.get('id')
        self.week_id = data.get('week_id')
        self.daynumber = data.get('daynumber')
        self.completed = data.get('completed', False)
        self.RPE = data.get('RPE', 0)
        self.usernotes = data.get('usernotes', '')
        self.workouts = [] # Can be multiple workouts in a day
        self.week = None

    def add_workout(self, workout):
        self.workouts.append(workout)

    def get_all_workouts(self):
        self.workouts = workout_module.Workout.get_all_by_day_id(self.id)
        return self.workouts

    @classmethod
    def create_day(cls, data):
        query = """
            INSERT INTO days (
                week_id,
                daynumber,
                completed,
                RPE,
                usernotes
            )
            VALUES (
                %(week_id)s,
                %(daynumber)s,
                %(completed)s,
                %(RPE)s,
                %(usernotes)s
            )
        """
        return connectToMySQL('workout_tracker_schema').query_db(query, data)
    
    @classmethod
    def get_all_by_week_id(cls, week_id):
        query = "SELECT * FROM days WHERE week_id = %(week_id)s;"
        data = {
            'week_id': week_id
        }

        results = connectToMySQL('workout_tracker_schema').query_db(query, data)

        days = []

        for row in results:
            days.append(cls(row))
        return days
    
    @classmethod
    def get_day_by_id(cls, day_id):
        query = "SELECT * FROM days WHERE id = %(id)s;"

        data = {
            'id': day_id
        }
        result = connectToMySQL('workout_tracker_schema').query_db(query, data)

        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def update_day(cls, data):
        query = """
            UPDATE days
            SET completed = %(completed)s,
                RPE = %(RPE)s,
                usernotes = %(usernotes)s
            WHERE id = %(id)s;
        """
        return connectToMySQL('workout_tracker_schema').query_db(query, data)

    
    @classmethod
    def delete_day(cls, day_id):
        query = "DELETE FROM days WHERE id = %(id)s;"

        data = {
            'id': day_id
        }

        return connectToMySQL('workout_tracker_schema').query_db(query, data)