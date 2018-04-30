from datetime import datetime, timedelta

class User():

    users = [
        {
            'id': 1,
            'user_name': u'james_katarikawe',
            'email': u'jpkatarikawe@gmail.com',
            'password': u'james', 
            'is_caterer': False,
            'orders_sent' : []
        },
        {
            'id': 2,
            'user_name': u'paul_kayongo',
            'email': u'paulkayongo@gmail.com',
            'password': u'kayongo', 
            'is_caterer': False,
            'orders_sent' : []
        },
        {
            'id': 3,
            'user_name': u'joseph_odur',
            'email': u'odur@gmail.com',
            'password': u'odur', 
            'is_caterer': True,
            'orders_received' : []
        },
        {
            'email': u'seryazi@gmail.com',
            'user_name': u'phillip_seryazi',
            
            'password': u'seryazi', 
            'is_caterer': True,
            'orders_received' : []
        }
    ]

    def save(self,user):
        # Adds user to collection of users
        self.users.append(user)

    def username_matches(self, username):
        # check if username is present
        if any(user['username'] == username for user in self.users):
            return True
        return False

    def email_matches(self, email):
        # check if email is present
        if any(user['email'] == email for user in self.users):
            return True
        return False

    def password_matches(self, password):
        # check if password is correct
        if any(user['password'] == password for user in self.users):
            return True
        return False