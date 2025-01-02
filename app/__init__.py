from flask import Flask
from pymongo import MongoClient
import os

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/weather_data")
client = MongoClient(MONGO_URI)
db = client["weather_data"]
collection = db["cities"]

# Import routes
from .api import *
