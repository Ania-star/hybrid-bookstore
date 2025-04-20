from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["hybrid_bookstore"]
recs = db["recommendations"]


def add_recommendation(doc):
    return recs.insert_one(doc)

def get_recommendations_by_user(user_id):
    return recs.find_one({"user_id": user_id})

def update_recommendations(user_id, book_ids):
    """
    Updates or inserts a user's recommended books list in MongoDB.
    """
    result = recs.update_one(
        {"user_id": user_id},
        {"$set": {"recommended_books": book_ids}},
        upsert=True
    )
    return {
        "user_id": user_id,
        "recommended_books": book_ids,
        "acknowledged": result.acknowledged,
        "modified_count": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None
    }
    

def delete_recommendation(user_id):
    return recs.delete_one({"user_id": user_id})
