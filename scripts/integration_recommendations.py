import sqlite3
from dotenv import load_dotenv
import os
import random

from scripts.crud_recommendations import update_recommendations
from scripts.crud_reviews import get_reviews_by_user
from scripts.crud_orders import get_all_orders
from scripts.crud_books import get_book_by_id

load_dotenv()
DB_PATH = "db/sql/hybrid_bookstore.db"


def generate_recommendations(user_id, min_rating=4):
    """
    Recommends up to 10 books based on categories from the user's order history and high-rated reviews.
    Stores recommendations in MongoDB using update_recommendations().
    """
    # Step 1: Get ordered book_ids and their categories
    ordered_books = []
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("""
            SELECT DISTINCT b.book_id, b.category_id
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            JOIN books b ON od.book_id = b.book_id
            WHERE o.user_id = ?
        """, (user_id,)).fetchall()
        ordered_books = rows

    ordered_book_ids = {r[0] for r in ordered_books}
    ordered_categories = {r[1] for r in ordered_books}

    # Step 2: Add categories from highly rated reviews (MongoDB -> SQLite)
    high_rated_reviews = get_reviews_by_user(user_id, min_rating)
    reviewed_book_ids = set()
    reviewed_categories = set()

    with sqlite3.connect(DB_PATH) as conn:
        for review in high_rated_reviews:
            reviewed_book_ids.add(review["book_id"])
            row = conn.execute("SELECT category_id FROM books WHERE book_id = ?", (review["book_id"],)).fetchone()
            if row:
                reviewed_categories.add(row[0])

    all_seen_books = ordered_book_ids.union(reviewed_book_ids)
    all_preferred_categories = ordered_categories.union(reviewed_categories)

    # Step 3: Recommend books from those categories the user hasn't seen
    with sqlite3.connect(DB_PATH) as conn:
        if not all_preferred_categories:
            return []

        placeholders = ",".join(["?"] * len(all_preferred_categories))
        result = conn.execute(f"""
            SELECT book_id FROM books
            WHERE category_id IN ({placeholders})
        """, tuple(all_preferred_categories)).fetchall()

    recommended_books = [r[0] for r in result if r[0] not in all_seen_books]
    random.shuffle(recommended_books)
    recommended_books = recommended_books[:10]

    # Step 4: Store to MongoDB
    update_recommendations(user_id, recommended_books)

    print(f"[recommendation] Ordered books: {ordered_book_ids}")
    print(f"[recommendation] Preferred categories: {all_preferred_categories}")
    print(f"[recommendation] Suggested: {recommended_books}")

    if not recommended_books:
        return []
    else:
        return {
            "user_id": user_id,
            "recommended_books": recommended_books,
            "categories_considered": list(all_preferred_categories),
            "books_seen": list(all_seen_books)
        }
