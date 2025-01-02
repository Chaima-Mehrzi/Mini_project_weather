from pymongo import MongoClient
import random
from datetime import datetime, timedelta
import os

# 🌍 Connexion MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/weather_data")
client = MongoClient(MONGO_URI)
db = client["weather_data"]
collection = db["cities"]

# 🌡️ Températures moyennes réalistes pour décembre-janvier
CITY_WEATHER_RANGES = {
    "Paris": {"min": -2, "max": 8, "weather": ["Clear", "Clouds", "Rain", "Fog", "Snow"]},
    "London": {"min": 0, "max": 10, "weather": ["Clear", "Clouds", "Rain", "Fog"]},
    "New York": {"min": -5, "max": 5, "weather": ["Clear", "Snow", "Clouds"]},
    "Tokyo": {"min": 5, "max": 15, "weather": ["Clear", "Clouds", "Rain"]},
    "Sydney": {"min": 18, "max": 30, "weather": ["Clear", "Clouds", "Rain"]}
}

# 📅 Génération de données pour les 30 derniers jours
def generate_realistic_weather_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    for city, config in CITY_WEATHER_RANGES.items():
        print(f"🌍 Generating realistic weather data for {city}")
        current_date = start_date
        
        while current_date <= end_date:
            for hour in range(0, 24, 3):  # Points toutes les 3 heures
                weather = random.choice(config["weather"])
                temperature = round(random.uniform(config["min"], config["max"]), 2)
                humidity = random.randint(50, 100)
                precipitation = round(random.uniform(0, 5), 2) if weather == "Rain" else 0
                
                weather_entry = {
                    "name": city,
                    "timestamp": (current_date + timedelta(hours=hour)).isoformat(),
                    "temperature": temperature,
                    "humidity": humidity,
                    "weather": weather,
                    "description": f"{weather.lower()} sky",
                    "precipitation": precipitation
                }
                
                collection.insert_one(weather_entry)
            current_date += timedelta(days=1)
        
        print(f"✅ Realistic data for {city} has been generated successfully!")

if __name__ == "__main__":
    generate_realistic_weather_data()
    print("✅ All cities have been populated with realistic weather data.")
