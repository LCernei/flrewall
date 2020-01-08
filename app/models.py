from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, login
from itertools import cycle
import base64
import json


class User(UserMixin):

    username = ""
    stored_password = ""
    blocked_domains = []
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.stored_password = xor_crypt_string(password, encode=True)
        # self.stored_password = generate_password_hash(password)

    def check_password(self, password):
        return self.stored_password == xor_crypt_string(password, encode=True)
        # return check_password_hash(self.stored_password, password)

    def get_id(self):
        return self.username

    @staticmethod
    def get(username):
        with open('data.json') as json_file:
            data = json.load(json_file)
            if username in data.keys():
                user = User()
                user.username = username
                user.stored_password = data[username]['stored_password']
                user.blocked_domains = data[username]['blocked_domains']
                return user
            else:
                return None

@login.user_loader
def load_user(id):
    return User.get(id)

def xor_crypt_string(data, key='my_secret_key', encode=False, decode=False):
    if decode:
        data = base64.decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
    if encode:
        return base64.encodestring(xored.encode("utf-8")).decode('ascii')
    return xored
