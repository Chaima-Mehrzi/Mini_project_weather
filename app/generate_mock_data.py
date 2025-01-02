from pymongo import MongoClient
import random
from datetime import datetime, timedelta

# MongoDB Connection
MONGO_URI = "mongodb://mongodb:27017/weather_data"
client = MongoClient(MONGO_URI)
db = client["weather_data"]
collection = db["cities"]

cities = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]
weather_conditions = ["Clear", "Rain", "Clouds", "Mist", "Fog"]

start_date = datetime.now() - timedelta(days=7)
data = []

for city in cities:
    for i in range(50):
        entry = {
            "name": city,
            "timestamp": (start_date + timedelta(hours=i)).isoformat(),
            "temperature": round(random.uniform(5, 25), 2),
            "weather": random.choice(weather_conditions)
        }
        data.append(entry)

collection.insert_many(data)
print("✅ Mock data inserted!")
