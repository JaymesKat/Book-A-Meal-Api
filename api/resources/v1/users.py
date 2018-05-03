from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

class UserObject(object):
    def __init__(self, id, email,user_name,first_name, last_name, is_caterer, password):
        self.id = id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.is_caterer = is_caterer
        self.email = email
        self.password = password

class User():
    users = [
        {
            'id': 1,
            'first_name': 'James',
            'last_name': 'Katarikawe',
            'user_name': 'james_katarikawe',
            'email': 'jpkatarikawe@gmail.com',
            'password': 'james', 
            'is_caterer': False
        },
        {
            'id': 2,
            'first_name': 'Paul',
            'last_name': 'Kayongo',
            'user_name': 'paul_kayongo',
            'email': 'paulkayongo@gmail.com',
            'password': 'kayongo', 
            'is_caterer': False
        },
        {
            'id': 3,
            'first_name': 'Joseph',
            'last_name': 'Odur',
            'user_name': 'joseph_odur',
            'email': 'odur@gmail.com',
            'password': 'odur', 
            'is_caterer': True
        },
        {
            'id': 4,
            'first_name': 'Phillip',
            'last_name': 'Seryazi',
            'email': 'seryazi@gmail.com',
            'user_name': 'phillip_seryazi',            
            'password': 'seryazi', 
            'is_caterer': True
        }
    ]

    @classmethod
    def register(cls, first_name, last_name, user_name, email, password):
        user = {'id': cls.users[-1]['id'] + 1,'first_name': first_name,'last_name': last_name,'user_name': user_name, 'email': email, 'password': password, 'is_caterer': False}
        cls.users.append(user)

    @classmethod
    def get_user(cls, email, password):    
        for each_user in cls.users:
            if email == each_user['email'] and password == each_user['password']:
                user = UserObject(each_user['id'],each_user['email'],each_user['user_name'],each_user['first_name'],each_user['last_name'],each_user['is_caterer'],each_user['password'])
                if user:
                    return user
                else:
                    return None
        return None            

    @classmethod
    def username_matches(cls, username):
        # check if username is present
        if any(user['user_name'] == username for user in cls.users):
            return True
        return False

    @classmethod
    def email_matches(cls, email):
        # check if email is present
        if any(user['email'] == email for user in cls.users):
            return True
        return False

    @classmethod
    def password_matches(cls, password):
        # check if password is correct
        if any(user['password'] == password for user in cls.users):
            return True
        return False