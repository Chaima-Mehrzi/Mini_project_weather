from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/")
    print(client.list_database_names())
    print("✅ Connexion réussie à MongoDB")
except Exception as e:
    print(f"❌ Erreur : {e}")
