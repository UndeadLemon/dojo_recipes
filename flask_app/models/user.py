from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
import re
bcrypt=Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

class User:
    def __init__(self,data):
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.birthday=data['birthday']
        self.id=data['id']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.password=data['password']
    @classmethod
    def save(cls, data):
        
        

        query = "INSERT INTO users (first_name, last_name, email, birthday, password, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(birthday)s, %(password)s, NOW(), NOW() );"

        return connectToMySQL('login_and_registration').query_db(query, data)
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id=%(id)s"

        return connectToMySQL('login_and_registration').query_db(query, data)
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at=NOW() WHERE id=%(id)s"

        return connectToMySQL('login_and_registration').query_db(query, data)
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login_and_registration').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    @classmethod
    def get_one(cls, data):
        query= "SELECT * FROM users WHERE id = %(id)s"

        return connectToMySQL('login_and_registration').query_db(query, data)
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"


        results = connectToMySQL('login_and_registration').query_db(query)

        users = []

        for user in results:
            users.append( cls(user) )
        return users

    @staticmethod
    def validate_user( user ):
        is_valid=True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid=False
        if len(user['last_name']) < 2 or len(user['first_name']) < 2:
            flash("First or Last Name is too short!")
            is_valid=False
        if not PASSWORD_REGEX.match(user['password']):
            flash('Invalid Password! Password must be at least 8 characters, and contain at least 1 special character, number, and capital letter!')
            is_valid=False
        return is_valid