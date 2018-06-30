from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


class UserResource():

    @classmethod
    def get_user_by_id(cls, user_id): 
            for each_user in cls.users:
                if user_id == each_user['id']:
                    return each_user   
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

    @staticmethod
    def email_is_valid(email):
        is_valid = validate_email(email)
        return is_valid
