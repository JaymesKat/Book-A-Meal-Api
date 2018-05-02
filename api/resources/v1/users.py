from datetime import datetime, timedelta

class User():

    users = [
        {
            'id': 1,
            'user_name': 'james_katarikawe',
            'email': 'jpkatarikawe@gmail.com',
            'password': 'james', 
            'is_caterer': False,
            'isloggedin': False
        },
        {
            'id': 2,
            'user_name': 'paul_kayongo',
            'email': 'paulkayongo@gmail.com',
            'password': 'kayongo', 
            'is_caterer': False,
            'isloggedin': False
        },
        {
            'id': 3,
            'user_name': 'joseph_odur',
            'email': 'odur@gmail.com',
            'password': 'odur', 
            'is_caterer': True,
            'isloggedin': False
        },
        {
            'id': 4,
            'email': 'seryazi@gmail.com',
            'user_name': 'phillip_seryazi',            
            'password': 'seryazi', 
            'is_caterer': True,
            'isloggedin': False
        }
    ]

    @classmethod
    def register(cls, first_name, last_name, user_name, email, password):
        user = {'id': cls.users[-1]['id'] + 1,'user_name': user_name, 'email': email, 'password': password, 'is_caterer': False}
        cls.users.append(user)

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