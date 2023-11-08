from flask import request
from flask_app.config.mysqlconnection import connectToMySQL


class User:
    def __init__(self, data) -> None:
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #CRUD Functions

    # Create
    @classmethod
    def create_user(cls, data):
        query = """
            INSERT INTO users (
                first_name,
                last_name,
                email,
                password,
                created_at,
                updated_at
            )
            VALUES (
                %(first_name)s,
                %(last_name)s,
                %(email)s,
                %(password)s,
                NOW(),
                NOW()
            );
        """
        return connectToMySQL('workout_tracker_schema').query_db(query, data)
    

    # Get All
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL('workout_tracker_schema').query_db(query)

        users = []

        for row in results:
            users.append(cls(row))
        return users
    
    # Get one by id
    @classmethod
    def get_one_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        data = {
            'id' : user_id
        }

        result = connectToMySQL('workout_tracker_schema').query_db(query, data)

        if result:
            return cls(result[0])
        else:
            return "User not found", None

    # Get one by email
    @classmethod
    def get_one_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        data = {
            'email' : email
        }

        result = connectToMySQL('workout_tracker_schema').query_db(query, data)

        if result:
            return cls(result[0])
        else:
            return "User not found", None

