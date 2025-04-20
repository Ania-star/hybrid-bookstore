from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["hybrid_bookstore"]
reviews = db["reviews"]




def add_review(review_data):
    return reviews.insert_one(review_data)

def get_reviews_by_user(user_id, min_rating=None):
    query = {"user_id": user_id}
    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}
    return list(reviews.find(query))


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
