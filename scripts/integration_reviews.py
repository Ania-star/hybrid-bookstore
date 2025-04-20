from datetime import datetime
from scripts.crud_reviews import add_review
from scripts.integration_recommendations import generate_recommendations
from scripts.crud_books import update_book_rating


import sqlite3
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DB_PATH = "db/sql/hybrid_bookstore.db"

client = MongoClient(os.getenv("MONGO_URI"))
db = client["hybrid_bookstore"]
reviews_col = db["reviews"]

def get_books_to_review(user_id):
    """
    Returns a list of book_ids the user has ordered but not yet reviewed.
    """
    # Get all ordered books
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT DISTINCT od.book_id
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            WHERE o.user_id = ?
        """, (user_id,)).fetchall()

    ordered_books = {row[0] for row in rows}

    # Get reviewed books from MongoDB
    reviewed_books = {doc["book_id"] for doc in reviews_col.find({"user_id": user_id})}

    return list(ordered_books - reviewed_books)

def submit_review(user_id, book_id, rating, text):
    """
    Submits a review for a book by a specific user.
    """
    review = {
        "user_id": user_id,
        "book_id": book_id,
        "rating": rating,
        "review_text": text,
        "timestamp": datetime.utcnow().isoformat()
    }

    #Update recommendations after review
    generate_recommendations(user_id)

    result = add_review(review)
    existing = list(reviews_col.find({"book_id": book_id}))
    ratings = [r["rating"] for r in existing]
    new_avg = round(sum(ratings) / len(ratings), 2)

    # update star_rating in SQL
    update_book_rating(book_id, new_avg)
    return {"status": "submitted", "review_id": str(result.inserted_id)}



def get_review_stats():
    pipeline = [
        {
            "$group": {
                "_id": "$book_id",
                "count": {"$sum": 1},
                "avg_rating": {"$avg": "$rating"}
            }
        }
    ]
    results = list(reviews_col.aggregate(pipeline))
    return {
        r["_id"]: {"count": r["count"], "avg_rating": round(r["avg_rating"], 2)}
        for r in results
    }