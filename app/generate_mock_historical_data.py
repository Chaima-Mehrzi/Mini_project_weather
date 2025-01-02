from pymongo import MongoClient
import random
from datetime import datetime, timedelta
import os

# Configuration MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/weather_data")
client = MongoClient(MONGO_URI)
db = client["weather_data"]
collection = db["cities"]

# Liste des villes avec des paramètres réalistes
CITIES = ["New York", "London", "Paris", "Tokyo", "Sydney"]

# Conditions météo possibles
WEATHER_CONDITIONS = ["Clear", "Rain", "Clouds", "Snow", "Fog"]
DESCRIPTIONS = {
    "Clear": "clear sky",
    "Rain": "light rain",
    "Clouds": "few clouds",
    "Snow": "light snow",
    "Fog": "foggy"
}

# Génération des données pour un mois
def generate_mock_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    for city in CITIES:
        print(f"🌆 Generating data for {city}")
        current_date = start_date
        
        while current_date <= end_date:
            for hour in range(0, 24, 3):  # Points toutes les 3 heures
                weather = random.choice(WEATHER_CONDITIONS)
                entry = {
                    "name": city,
                    "temperature": round(random.uniform(5, 35), 2),
                    "humidity": random.randint(30, 90),
                    "weather": weather,
                    "description": DESCRIPTIONS[weather],
                    "timestamp": (current_date + timedelta(hours=hour)).isoformat()
                }
                collection.insert_one(entry)
            current_date += timedelta(days=1)
        
        print(f"✅ Data generated for {city}")

if __name__ == "__main__":
    generate_mock_data()
    print("✅ Mock historical weather data generation complete.")
