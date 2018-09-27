from flask import Flask, send_from_directory, request, Response
import os
import bcrypt
import pymongo
import jwt
import re

# Use the dist/ directory as the static files directory.
app = Flask(__name__,
            root_path=os.path.realpath(os.path.pardir) + '/WebApp',
            static_folder='dist',
            static_url_path='/')
client = pymongo.MongoClient('localhost', 27017)
db = client.get_database('student_modeling')
illegal_chars_regex = re.compile(r'[!@#$%^&*()+\-=[\]{};\':"\\|,.<>/?]')
secret = 'skjszd*A87yjhdkjszdhkl@#U8ukSH@*#&238232398'


@app.route('/api/user/signup', methods=['POST'])
def user_signup():
    """
    Handles the user signup. Accepts a JSON object with
    {
        username: string,
        name: string,
        password: string
    }
    Hashes the password with bcrypt using a salt, and adds to the
    database if the username does not already exist. If successful,
    returns a 200 OK with the syntax
    {
        success: true,
        token: string
    }
    where token is a JSON Web Token. If the username exists, the
    response returns a 409 Conflict, with the body:
    {
        success: false,
        error: string
    }
    """
    # Get request parameters
    data = request.get_json()
    username = data['username']
    name = data['name']
    pwd = data['password']

    # Check basic errors
    if username is None or name is None or pwd is None or \
            username.isspace() or name.isspace() or pwd.isspace():
        return Response('{"success":false, error:"Invalid parameters"}',
                        status=400, mimetype='application/json')

    if illegal_chars_regex.match(username) or illegal_chars_regex.match(name):
        return Response('{"success":false, error:"Invalid characters"}',
                        status=400, mimetype='application/json')

    if ' ' in username:
        error_msg = '{"success":false, error:"Username cannot have spaces"}'
        return Response(error_msg, status=400, mimetype='application/json')

    # Hash the password with salt
    hashed = bcrypt.hashpw(pwd.encode('utf8'), bcrypt.gensalt())

    user_coll = db.get_collection('users')

    # Get a list of colliding usernames
    colliding_usernames = user_coll.find_one({
        'username': username
    })
    if colliding_usernames is None:
        # No collisions, we can insert
        user_coll.insert_one({
            'username': username,
            'name': name,
            'password': hashed.decode('utf8')
        })

        # Generate a token and respond with a 200 OK.
        encoded = jwt.encode({
            'username': username,
            'name': name
        }, secret, headers={
            'expiresIn': '1 day'
        })

        succ_res = '{"success":true, "token":"' + encoded.decode('utf8') + '"}'
        return Response(succ_res, status=200, mimetype='application/json')
    else:
        # There were collisions, respond with a 409 Conflict
        return Response('{"success":false}', status=409,
                        mimetype='application/json')


@app.route('/api/user/login', methods=['POST'])
def user_login():
    """
    Implements user login. Accepts credentials as
    {
        username: string,
        password: string
    }
    If the authentication details succeed,
    then creates a JWT and returns it to the client with a 200 OK.
    The success response is
    {
        success: true,
        token: string
    }
    In case of auth failure, a 401 Unauthorized is returned.
    {
        success: false,
        error: string
    }
    """
    data = request.get_json()
    username = data['username']
    pwd = data['password']

    user_coll = db.get_collection('users')
    matched_user = user_coll.find_one({
        'username': username
    })
    if matched_user is None:
        # Username does not exist. Give a vague error for
        # security reasons.
        return Response('{"success":false,"error":"Invalid credentials"}',
                        status=401, mimetype='application/json')
    else:
        if bcrypt.checkpw(pwd.encode('utf8'),
                          matched_user['password'].encode('utf8')):
            # Auth successful
            encoded = jwt.encode({
                'username': username,
                'name': matched_user['name']
            }, secret, headers={
                'expiresIn': '1 day'
            })
            succ_res = '{"success":true, "token":"' + \
                encoded.decode('utf8') + '"}'
            return Response(succ_res, status=200, mimetype='application/json')
        else:
            # Auth failure
            return Response('{"success":false,"error":"Invalid credentials"}',
                            status=401, mimetype='application/json')


@app.route('/api/user/details', methods=['POST'])
def user_details():
    """
    Accepts a JWT, decodes it, checks its validity, and returns user details.
    Accepts a token
    {
        token: string
    }
    Returns a 200 OK for successful attempts, with
    {
        success: true,
        decoded: JSON object
    }
    If the token is invalid or has expired, returns a 401 Unauthorized
    {
        success: false,
        error: string
    }
    """
    data = request.get_json()
    token = data['token']

    try:
        decoded = jwt.decode(token, key=secret)
        return Response('{"success":true,"decoded":"' + str(decoded) + '"}',
                        status=200, mimetype='application/json')
    except Exception:
        response = '{"success":false, "error": "Invalid token"}'
        return Response(response, status=401, mimetype='application/json')


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def static_files(path):
    """
    Static files handler. / defaults to index.html, and the
    other files are matched via the expression.
    """
    return app.send_static_file(path)
