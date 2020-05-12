from flask_pymongo import PyMongo
from app import app

app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/firstdb"
mongo = PyMongo(app)