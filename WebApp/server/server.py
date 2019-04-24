from flask import Flask, send_from_directory, request, Response
import os
import bcrypt
import pymongo
import jwt
import re
import datetime
import json
from bson.objectid import ObjectId
import numpy as np

from BKT import BKT
from AdaptiveTester import AdaptiveTester

from catsim.cat import generate_item_bank
from catsim.initialization import RandomInitializer
from catsim.selection import UrrySelector, IntervalInfoSelector
from catsim.estimation import HillClimbingEstimator
from catsim.simulation import Simulator

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


@app.route('/api/session/submit', methods=['POST'])
def submit_response():
    """
    Adds a user response to the database. Takes
    {
        question_id: The question ID from the questions collection
        response: User's response, int
        correct: Correct answer, int,
        token: string
    }
    Returns 401 if token is invalid, and 200 otherwise.
    """
    data = request.get_json()
    qid = data['question_id']
    response = data['response']
    answer = data['correct']
    token = data['token']

    # Get concept name for convenience later
    ques_coll = db.get_collection('questions')
    concept = ques_coll.find_one({'_id': ObjectId(qid)})['concept']

    # Get the username from the JWT
    try:
        decoded = jwt.decode(token, key=secret)
        username = decoded['username']
    except Exception:
        response = '{"success":false, "error": "Invalid token"}'
        return Response(response, status=401, mimetype='application/json')

    # Insert all the data
    responses_coll = db.get_collection('responses')
    responses_coll.insert_one({
        'question_id': qid,
        'response': int(response),
        'answer': int(answer),
        'date': datetime.datetime.now().isoformat(),
        'username': username,
        'concept': concept
    })
    return Response('{"success": true}', status=200,
                    mimetype='application/json')


@app.route('/api/concepts/list', methods=['GET'])
def list_concepts():
    """
    Returns a list of all concepts.
    """
    # Get all questions
    ques_coll = db.get_collection('questions')
    docs = ques_coll.find({}, projection=['concept'])
    docs = list(docs)

    # Filter out only the concept and extract unique concepts
    concepts = list(map(lambda x: x['concept'], docs))
    uniq_concepts = list(set(concepts))

    return_doc = json.dumps({'concepts': uniq_concepts})
    return Response(return_doc, status=200, mimetype='application/json')


@app.route('/api/session/get_question', methods=['POST'])
def fetch_question():
    """
    Gets the next question, given the user and concept name. Takes JSON
    {
        token: str,
        concept: str
    }
    and returns a document from the MongoDB database. Sends 401 if the
    token is invalid
    """
    data = request.get_json()
    token = data['token']
    concept = data['concept']

    # Decode the JWT to get the username
    try:
        decoded = jwt.decode(token, key=secret)
        username = decoded['username']
    except Exception:
        response = '{"success":false, "error": "Invalid token"}'
        return Response(response, status=401, mimetype='application/json')

    # Get a list of the questions to get the bank size and the list of items
    ques_coll = db.get_collection('questions')
    concept_questions = list(ques_coll.find({'concept': concept}))

    # Get a list of user responses (correct or incorrect), and also extract
    # the list of administered questions
    responses_coll = db.get_collection('responses')
    user_responses = list(
        responses_coll.find({'username': username, 'concept': concept})
    )

    # To get the administered questions, first sort by date. But we need
    # INDICES, or INTEGERS, not _ids!
    administered_items = sorted(user_responses, key=lambda x: x['date'])
    responses = list(
        map(lambda x: x['answer'] == x['response'], administered_items)
    )
    
    # Get indices--we need an array of indices of administered items.
    # These indices are with respect to concept_questions.
    concept_ids = list(
        map(lambda obj: str(obj['_id']), concept_questions)
    )
    administered_ids = list(
        map(lambda obj: str(obj['question_id']), administered_items)
    )

    # Now, convert to numpy arrays
    concept_ids = np.array(concept_ids)
    administered_ids = np.array(administered_ids)

    # Now, get the indices. For each item x in administered_ids, find the
    # index of x in concept_ids.
    indices = list(
        map(lambda x: np.where(concept_ids == x)[0][0], administered_ids)
    )

    selector = AdaptiveTester(item_count=len(concept_questions),
                              administered=indices,
                              responses=responses,
                              bucket_size=5)
    item_index = selector.get_next_question()

    # Now get the question that we need to return
    print('Index:', item_index)
    next_question = concept_questions[item_index]
    next_question['_id'] = str(next_question['_id'])

    return Response(json.dumps(next_question), status=200,
                    mimetype='application/json')


@app.route('/api/user/performance', methods=['POST'])
def get_concept_performance():
    """
    Gets a student's performance in a concept. Accepts POST request
    with data
    {
        concept: string,
        student: string, (username)
    }
    At the moment, no authentication mechanism for accessing this
    data is implemented.
    """
    data = request.get_json()
    concept = data['concept']
    username = data['student']

    responses_coll = db.get_collection('responses')
    user_responses = list(
        responses_coll.find({'username': username, 'concept': concept})
    )

    if len(user_responses) == 0:
        response = {
            'success': False,
            'error': 'No data for this student and concept'
        }
        return Response(json.dumps(response), status=200,
                        mimetype='application/json')

    correct_responses = list(map(lambda x: int(x['answer'] == x['response']),
                                 user_responses))
    model = BKT(correct_responses)
    model.fit()
    start, transition, emission = model.get_model_params()

    response = {
        'success': True,
        'start_probs': start.tolist(),
        'transition_probs': transition.tolist(),
        'emission_probs': emission.tolist()
    }
    return Response(json.dumps(response), status=200,
                    mimetype='application/json')


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def static_files(path):
    """
    Static files handler. / defaults to index.html, and the
    other files are matched via the expression.
    """
    return app.send_static_file(path)
