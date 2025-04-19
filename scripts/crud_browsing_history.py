from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["hybrid_bookstore"]
history = db["browsing_history"]

# Index for performance
history.create_index("user_id")

def add_history_entry(entry):
    return history.insert_one(entry)

def get_history_by_user(user_id):
    return list(history.find({"user_id": user_id}))

def delete_history_entry(user_id, book_id):
    return history.delete_one({"user_id": user_id, "book_id": book_id})
