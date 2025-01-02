
import requests
import os
from pymongo import MongoClient
from datetime import datetime

# 🔧 MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/weather_data")
client = MongoClient(MONGO_URI)
db = client["weather_data"]
collection = db["cities"]

# 🔑 OpenWeather API Configuration
API_KEY = "your_actual_api_key"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    try:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric&lang=en"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        weather_data = {
            "name": city,
            "temperature": data['main']['temp'],
            "weather": data['weather'][0]['main'],
            "description": data['weather'][0]['description'],
            "timestamp": datetime.now()
        }
        
        collection.update_one({"name": city}, {"$set": weather_data}, upsert=True)
        print(f"✅ Weather data updated for {city}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def fetch_multiple_cities():
    cities = ["New York", "London", "Paris", "Tokyo", "Sydney"]
    for city in cities:
        fetch_weather(city)

if __name__ == "__main__":
    print("🌍 Fetching Weather Data...")
    fetch_multiple_cities()
    print("✅ Weather Data Fetching Complete.")
