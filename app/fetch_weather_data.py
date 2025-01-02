import requests
from pymongo import MongoClient
from datetime import datetime, timedelta
import os

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/weather_data")
client = MongoClient(MONGO_URI)
db = client["weather_data"]
collection = db["cities"]

# OpenWeather API Configuration
API_KEY = "f38f9be30e7977402bbc4e1ed4596e9d"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    try:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        weather_data = {
            "name": city,
            "temperature": data['main']['temp'],
            "weather": data['weather'][0]['main'],
            "description": data['weather'][0]['description'],
            "timestamp": datetime.now()
        }
        
        collection.insert_one(weather_data)
        print(f"✅ Data added for {city}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Fetch historical data for the last 7 days
def fetch_historical_data():
    cities = ["New York", "London", "Paris", "Tokyo", "Sydney"]
    for city in cities:
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            fetch_weather(city)

if __name__ == "__main__":
    fetch_historical_data()
