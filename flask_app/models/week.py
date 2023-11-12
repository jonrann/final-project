from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL

class Week:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.program_id = data['program_id']
        self.weeknumber = data['weeknumber']

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
    def get_all_weeks_from_program_id(cls, program_id):
        query = "SELECT * FROM weeks WHERE program_id = %(program_id)s;"

        data = {
            'id': program_id
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