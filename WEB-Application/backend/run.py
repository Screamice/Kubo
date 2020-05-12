from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from bson import json_util, ObjectId

APP = Flask(__name__)

# ---------------------------------------------------------------------------------------------------------------------------#
# Flask Settings
APP.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/pythonreactdb'
mongo = PyMongo(APP)

DB = mongo.db.users

CORS(APP)

# ----------------------------------------------------------------------------------------------------------------------------#
# Routes
@APP.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return get_all_lusers()
    
    elif request.method == "POST":
        return create_user()

@APP.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def get_user_info(user_id):
    if request.method == "GET":
        return get_user(user_id)
    
    elif request.method == "PUT":
        return update_user(user_id)

    elif request.method == "DELETE":
        return delete_user(user_id)

@APP.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

# ------------------------------------------------------------------------------------------------------------------#
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    
    if username and password and email:
        hashed_password = generate_password_hash(password)
        id = DB.insert({
            "username": username,
            "password": hashed_password,
            "email": email
        })
        return jsonify({
            "message": "New user added successfully",
            'id': str(id)
        })
    return jsonify({
        "message": "Couldn't add the user, the data is not complete"
    })

def get_all_lusers():
    users = []
    for match in DB.find():
        users.append({
            '_id': str(ObjectId(match['_id'])),
            'username': match['username'],
            'email': match['email'],
            'password': match['password']
        })
    return jsonify(users)

def get_user(user_id):
    user = DB.find_one({'_id': ObjectId(user_id)})
    response = jsonify({
        '_id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'password': user['password']
    })
    return response

def update_user(user_id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        hashed_password = generate_password_hash(password)
        DB.update_one({'_id': ObjectId(user_id)}, {'$set': {
            'username': username,
            'password': hashed_password,
            'email': email
        }})
        response = jsonify({'message': 'The user '+ user_id + ' was updated'})
        return response

def delete_user(user_id):
    DB.delete_one({'_id': ObjectId(user_id)})
    response = jsonify({
        "message": "The user " + user_id + "was deleted"
    })
    return response

# ------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    APP.run(debug=True)