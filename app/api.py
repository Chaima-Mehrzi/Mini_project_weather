from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
from datetime import datetime

# Initialize Flask App
app = Flask(__name__)

# MongoDB Connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017/weather_data")
client = MongoClient(MONGO_URL)
db = client.weather_data
collection = db.cities

@app.route('/cities', methods=['GET'])
def get_cities():
    try:
        cities = list(collection.find({}, {"_id": 0, "name": 1, "temperature": 1, "weather": 1}))
        return jsonify(cities)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cities/<city>', methods=['GET'])
def get_city_data(city):
    try:
        city_data = list(collection.find({"name": city}, {"_id": 0}))
        return jsonify(city_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
