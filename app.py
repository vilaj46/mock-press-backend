import os
import jwt
import time
import pymongo
from flask_cors import CORS
from itsdangerous import json
from flask import Flask, make_response, request

# https://gist.github.com/prahladyeri/0b92b9ca837a0f5474c732876220db78

# Classes
from classes.Admin import Admin
from classes.Goggles import Goggles

# Utilities
# Delete this function
# from utilities.authentication.set_cookie import set_cookie
# Jie Jen
# from frontend import * not found when deployed.

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# app.config['MONGO_URI'] = 'mongodb+srv://vilaj46:4ex2j842adji888@cluster0.djhoa.mongodb.net/myFirstDatabase'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['DB_NAME'] = 'mongodb+srv://vilaj46:4ex2j842adji888@cluster0.djhoa.mongodb.net/myFirstDatabase'
app.config['UPLOAD_FOLDER'] = "./tmp"
DB_NAME = 'mongodb+srv://vilaj46:4ex2j842adji888@cluster0.djhoa.mongodb.net/myFirstDatabase'
my_client = pymongo.MongoClient(DB_NAME)


@app.route('/')
def index():
    return '<p>Hello, World!</p>'


@app.route('/google')
def google():
    return '<h1>Google</h1>'


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    google_auth = Goggles(uploaded_file)
    file_name = google_auth.save_to_drive()
    # # Remove file from temporary files.
    tmp_files = os.listdir('./tmp')
    while file_name in tmp_files:
        try:
            os.remove('./tmp/{0}'.format(file_name))
        except:
            # Do nothing.
            print('Deleting...')
            tmp_files = os.listdir('./tmp')
    return {}


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = Admin.login(username, password)
        return response
    else:
        # Method is GET.
        token = request.headers.get('Authorization').split(" ")[1]

        # Check if token expires
        decoded = jwt.decode(token, "secretsecret", algorithms=["HS256"])

        # date_now = datetime.utcnow()
        # print(date_now)
        current_time = time.time() * 1000
        milli = decoded['exp'] * 1000

        try:
            expired = current_time >= milli
            if expired == True:
                response = make_response({
                    'message': 'Invalid token'
                })
                return response, 401
            else:
                db_name = my_client['users']
                collection_name = db_name['admins']
                admins = collection_name.find({})
                admins_list = []
                for a in admins:
                    admins_list.append(a['username'])

                return {'admins': admins_list}
        except:
            response = make_response({
                'message': 'Invalid token'
            })
            return response, 401
