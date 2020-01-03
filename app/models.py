from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, login
import json


class User(UserMixin):

    username = ""
    password_hash = ""
    blocked_domains = []
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

    @staticmethod
    def get(username):
        with open('data.json') as json_file:
            data = json.load(json_file)
            if username in data.keys():
                user = User()
                user.username = username
                user.password_hash = data[username]['password_hash']
                user.blocked_domains = data[username]['blocked_domains']
                return user
            else:
                return None

@login.user_loader
def load_user(id):
    return User.get(id)
