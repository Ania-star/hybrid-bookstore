from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["hybrid_bookstore"]
reviews_col = db["reviews"]
profiles_col = db["customer_profiles"]

def get_top_reviewers(min_reviews=3, min_rating=4.0):
    pipeline = [
        {
            "$group": {
                "_id": "$user_id",
                "review_count": {"$sum": 1},
                "avg_rating": {"$avg": "$rating"}
            }
        },
        {
            "$match": {
                "review_count": {"$gte": min_reviews},
                "avg_rating": {"$gte": min_rating}
            }
        }
    ]
    return list(reviews_col.aggregate(pipeline))

def get_top_reviewers_with_locations():
    top_reviewers = get_top_reviewers()
    user_ids = [r["_id"] for r in top_reviewers]

    profiles = profiles_col.find({"user_id": {"$in": user_ids}})
    profile_dict = {p["user_id"]: p for p in profiles}

    results = []
    for reviewer in top_reviewers:
        user_id = reviewer["_id"]
        profile = profile_dict.get(user_id)
        if profile and "coordinates" in profile:
            coords = profile["coordinates"]["coordinates"]
            results.append({
                "user_id": user_id,
                "lat": coords[1],
                "lon": coords[0],
                "avg_rating": round(reviewer["avg_rating"], 2),
                "review_count": reviewer["review_count"],
                "address": profile.get("address", {})
            })

    return results
