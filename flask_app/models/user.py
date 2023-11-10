from flask import request, flash
from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data) -> None:
        self.id = data['id']
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


    # Validator
    @staticmethod
    def validate_user(data):
        is_valid = True
        # Validate first name
        if len(data['first_name']) < 3:
            flash('First name needs to be at least 3 characters', 'register_error')
            is_valid = False

        # Validate last name
        if len(data['last_name']) < 3:
            flash('Last name needs to be at least 3 characters', 'register_error')
            is_valid = False

        # Validate email
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email', 'register_error')
            is_valid = False

        # Validate password
        if len(data['password']) < 5:
            flash('Password needs to be at least 3 characters', 'register_error')
            is_valid = False
        if not re.search("[A-Z]", data['password']):
            flash('Password needs at least 1 capital letter', 'register_error')
            is_valid = False
        if not re.search("[0-9]", data['password']):
            flash('Password needs at least 1 number', 'register_error')
            is_valid = False

        # Validate confirme password
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match', 'register_error')
            is_valid = False
        return is_valid