from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["hybrid_bookstore"]
recs = db["recommendations"]

# Unique per user
recs.create_index("user_id", unique=True)

def add_recommendation(doc):
    return recs.insert_one(doc)

def get_recommendations_by_user(user_id):
    return recs.find_one({"user_id": user_id})

def update_recommendations(user_id, book_ids):
    return recs.update_one(
        {"user_id": user_id},
        {"$set": {"recommended_books": book_ids}}
    )

def delete_recommendation(user_id):
    return recs.delete_one({"user_id": user_id})
