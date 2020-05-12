from flask import request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from app.model.connection import mongo
from app import app

@app.route("/", methods=["GET"])
def index():
    return "Hola"

@app.route("/users", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']

        if username and password and email:
            hashed_password = generate_password_hash(password)
            id = mongo.db.users.insert({
                'username': username,
                'password': hashed_password,
                'email': email
            })
            response = {
                'id': str(id),
                'username': username,
                'password': hashed_password,
                'email': email
            }
            return response
        else:
            return not_found()

    elif request.method == "GET":
        users = mongo.db.users.find()
        response = json_util.dumps(users)
        return Response(response, mimetype="application/json")

@app.route("/users/<id>", methods=["GET", "DELETE", "PUT"])
def get_user(id):
    if request.method == "GET":
        user = mongo.db.users.find_one({'_id': ObjectId(id)})
        response = json_util.dumps(user)
        return Response(response, mimetype="application/json")
    elif request.method == "DELETE":
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        response = jsonify({
            "message": "The user " + id + "was deleted"
        })
        return response
    elif request.method == "PUT":
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']

        if username and password and email:
            hashed_password = generate_password_hash(password)
            mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
                'username': username,
                'password': generate_password_hash(password),
                'email': email
            }})
            response = jsonify({'message': 'The user '+ id + ' was updated'})
            return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response
