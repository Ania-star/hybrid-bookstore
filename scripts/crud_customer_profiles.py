from pymongo import MongoClient, GEOSPHERE
from dotenv import load_dotenv
import os
print("✅ crud_customer_profiles.py loaded")
print("Available functions in this module:")
print(dir())

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["hybrid_bookstore"]
profiles = db["customer_profiles"]


def add_profile(profile_data):
    return profiles.insert_one(profile_data)

def get_profile_by_user(user_id):
    return profiles.find_one({"user_id": user_id})

def update_profile_rating(user_id, new_avg_rating):
    return profiles.update_one(
        {"user_id": user_id},
        {"$set": {"avg_rating_given": new_avg_rating}}
    )

def delete_profile(user_id):
    return profiles.delete_one({"user_id": user_id})

def find_users_near(lat, lon, max_distance_km=50):
    return list(profiles.find({
        "coordinates": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "$maxDistance": max_distance_km * 1000
            }
        }
    }))
