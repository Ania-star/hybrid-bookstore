"""
MongoDB Index Setup Script

Use this script to create indexes for all MongoDB collections.
Indexes improve query performance and are safe to run multiple times.

Run this ONLY when:
  - You clone the repo for the first time
  - You reset or clear the database
  - You add new collections or change indexed fields

Usage:
    python db/mongo/indexes.py
"""


from pymongo import MongoClient, GEOSPHERE
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["hybrid_bookstore"]

# Index definitions
print("Creating indexes for hybrid_bookstore collections...\n")

# customer_profiles
db.customer_profiles.create_index("user_id", unique=True)  # Ensure one profile per user
db.customer_profiles.create_index([("coordinates", GEOSPHERE)])  # For geo queries

# recommendations
db.recommendations.create_index("user_id", unique=True) # Unique per user

# reviews
db.reviews.create_index("user_id") # For get_reviews_by_user()
db.reviews.create_index("book_id") # For book-specific queries

# browsing_history
db.browsing_history.create_index("user_id") # Index for performance

print("\n Indexes successfully created (safe to re-run)")


