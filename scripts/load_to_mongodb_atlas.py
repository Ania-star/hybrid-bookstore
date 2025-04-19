import json
import os
from pymongo import MongoClient, GEOSPHERE
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get MongoDB connection string from .env
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

# === Ping test ===
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("MongoDB connection failed:", e)

# === Database ===
db = client["hybrid_bookstore"]

# === Collection file mapping ===
collections = {
    "customer_profiles": "data/customer_profiles.json",
    "recommendations": "data/recommendations.json",
    "browsing_history": "data/browsing_history.json",
    "reviews": "data/reviews.json"
}

# === Insert data into MongoDB ===
for collection_name, file_path in collections.items():
    print(f"Inserting {collection_name} from {file_path}...")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):  # single object
            data = [data]

    collection = db[collection_name]
    result = collection.insert_many(data)
    print(f"Inserted {len(result.inserted_ids)} documents into {collection_name}")

# === Create 2dsphere index for geolocation ===
print("Creating 2dsphere index on customer_profiles.coordinates...")
db["customer_profiles"].create_index([("coordinates", GEOSPHERE)])
print("Index created successfully.")
