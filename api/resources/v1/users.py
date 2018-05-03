from datetime import datetime, timedelta

class Person(object):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

class User(object):
    users = [
        {
            'id': 1,
            'user_name': 'james_katarikawe',
            'email': 'jpkatarikawe@gmail.com',
            'password': 'james', 
            'is_caterer': False
        },
        {
            'id': 2,
            'user_name': 'paul_kayongo',
            'email': 'paulkayongo@gmail.com',
            'password': 'kayongo', 
            'is_caterer': False
        },
        {
            'id': 3,
            'user_name': 'joseph_odur',
            'email': 'odur@gmail.com',
            'password': 'odur', 
            'is_caterer': True
        },
        {
            'id': 4,
            'email': 'seryazi@gmail.com',
            'user_name': 'phillip_seryazi',            
            'password': 'seryazi', 
            'is_caterer': True
        }
    ]

    @classmethod
    def register(cls, first_name, last_name, user_name, email, password):
        user = {'id': cls.users[-1]['id'] + 1,'user_name': user_name, 'email': email, 'password': password, 'is_caterer': False}
        cls.users.append(user)

    @classmethod
    def get_user(cls, email, password):    
        for each_user in cls.users:
            if cls.email_matches(email) and cls.password_matches(password):
                user = Person(each_user['id'],each_user['email'],each_user['password'])
                return user
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