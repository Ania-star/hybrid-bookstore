from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["hybrid_bookstore"]
reviews = db["reviews"]


# Add indexes 
reviews.create_index("user_id")  # For get_reviews_by_user()
reviews.create_index("book_id")  # For book-specific queries

def add_review(review_data):
    return reviews.insert_one(review_data)

def get_reviews_by_user(user_id):
    return list(reviews.find({"user_id": user_id}))

def update_review_rating(user_id, book_id, new_rating):
    return reviews.update_one(
        {"user_id": user_id, "book_id": book_id},
        {"$set": {"rating": new_rating}}
    )

def delete_review(user_id, book_id):
    return reviews.delete_one({"user_id": user_id, "book_id": book_id})

def get_reviews_by_book(book_id):
    return list(reviews.find({"book_id": book_id}))

print("crud_reviews.py loaded")
print("Functions available:", dir())
