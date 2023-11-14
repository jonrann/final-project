from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL

class Exercise:
    def __init__(self, data) -> None:
        self.id = data.get('id')
        self.workout_id = data.get('workout_id')
        self.title = data.get('title')
        self.content = data.get('content')
        self.workout = None

    
    @classmethod
    def create_exercise(cls, data):
        query = """
            INSERT INTO exercises (
                workout_id,
                title,
                content
            )
            VALUES (
                %(workout_id)s,
                %(title)s,
                %(content)s
            )
        """
        return connectToMySQL('workout_tracker_schema').query_db(query, data)
    
    @classmethod
    def get_exercise_by_id(cls, exercise_id):
        query = "SELECT * FROM exercises WHERE id = %(id)s;"

        data = {
            'id': exercise_id
        }
        result = connectToMySQL('workout_tracker_schema').query_db(query, data)

        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def get_all_by_workout_id(cls, workout_id):
        query = "SELECT * FROM exercises WHERE workout_id = %(workout_id)s;"
        data = {
            'workout_id': workout_id
        }

        results = connectToMySQL('workout_tracker_schema').query_db(query, data)

        exercises = []

        for row in results:
            exercises.append(cls(row))
        return exercises
    
    @classmethod
    def update_exercise(cls, data):
        query = """
            UPDATE exercises
            SET title = %(title)s,
                content = %(content)s
            WHERE id = %(id)s;
        """
        return connectToMySQL('workout_tracker_schema').query_db(query, data)
    
    @classmethod
    def delete_exercise(cls, exercise_id):
        query = "DELETE FROM exercises WHERE id = %(id)s;"
        
        data = {
            'id' : exercise_id
        }

        return connectToMySQL('workout_tracker_schema').query_db(query, data)
    