from flask import jsonify, make_response
from argon2 import PasswordHasher

from get_db import get_db

from classes.JWT import JWT


class Admin:
    username = ""
    password = ""
    is_admin = True

    def __init__(self, username, password):
        ph = PasswordHasher()
        password_hash = ph.hash(password)
        self.username = username
        self.password = password_hash

    def __str__(self):
        return self.username

    def to_json(self):
        return {
            'username': self.username,
            'password': self.password,
            'is_admin': self.is_admin
        }

    # Authentication
    def login(username, password):
        print(username)
        print(password)
        print('-----------------------')
        my_client = get_db()
        db_name = my_client['users']
        collection_name = db_name['admins']

        found_admin = collection_name.find_one({
            'username': username
        })

        success = is_valid_password(password, found_admin['password'])

        if success == False:
            error_json = {
                'message': 'Username or password incorrect.'
            }
            response = make_response(error_json)
            return response, 401

        admin_details = {}

        for k in found_admin:
            if k != '_id' and k != 'password':
                admin_details[k] = found_admin[k]

        encoded_jwt = JWT(admin_details)

        token = encoded_jwt.get()

        token_json = {
            "token": token
        }

        response = make_response(token_json)

        return response


def is_valid_password(potential_password, password_hash):
    ph = PasswordHasher()
    try:
        verified = ph.verify(password_hash, potential_password)
        if verified == True:
            return True
    except:
        return False
