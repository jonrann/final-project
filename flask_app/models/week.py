from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import day as day_module

class Week:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.program_id = data['program_id']
        self.weeknumber = data['weeknumber']
        self.days = []

    def add_day(self, day):
        self.days.append(day)

    def get_all_days(self):
        self.days = day_module.Day.get_all_by_week_id(self.id)
        return self.days

    # CRUD

    # Create
    @classmethod
    def create_week(cls, data):
        query = """
            INSERT INTO weeks (
                program_id,
                weeknumber
            )
            VALUES (
                %(program_id)s,
                %(weeknumber)s
            );
        """
        return connectToMySQL('workout_tracker_schema').query_db(query, data)

    @classmethod
    def get_all_by_program_id(cls, program_id):
        query = "SELECT * FROM weeks WHERE program_id = %(program_id)s;"
        data = {
            'program_id': program_id
        }

        results = connectToMySQL('workout_tracker_schema').query_db(query, data)

        weeks = []

        for row in results:
            weeks.append(cls(row))
        return weeks
    
    @classmethod
    def get_week_by_id(cls, week_id):
        query = "SELECT * FROM weeks WHERE id = %(id)s;"

        data = {
            'id': week_id
        }
        result = connectToMySQL('workout_tracker_schema').query_db(query, data)

        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def delete_week(cls, week_id):
        query = "DELETE FROM weeks WHERE id = %(id)s;"

        data = {
            'id': week_id
        }

        return connectToMySQL('workout_tracker_schema').query_db(query, data)
