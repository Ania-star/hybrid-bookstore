import os
from dotenv import load_dotenv
import requests  # Used for calling Google Maps API
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from scripts.crud_customers import insert_customer  # SQL helper
from scripts.crud_customer_profiles import add_profile  # MongoDB helper
from scripts.crud_customers import get_customer_by_id
from scripts.crud_customer_profiles import get_profile_by_user

# Load .env environment variables 
load_dotenv()

# Initialize MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["hybrid_bookstore"]

def geocode_address(address_dict):
    """Converts address fields to coordinates using Google Maps API"""
    address_str = ", ".join([v for v in address_dict.values() if v])
    print("Geocoding address (Google):", address_str)

    params = {
        "address": address_str,
        "key": os.getenv("GOOGLE_API_KEY")  # reads your key from .env
    }

    try:
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            print(f"Found location: ({location['lat']}, {location['lng']})")
            return [location["lng"], location["lat"]]  # MongoDB expects [lng, lat]
        else:
            print("Google API response:", data["status"])
    except Exception as e:
        print("Google Geocoding error:", e)

    return [0.0, 0.0]  # fallback if geocoding fails


def create_user_with_profile(user_data, profile_template=None):
    """
    Inserts a new user into SQL and creates a related MongoDB profile.
    Auto-generates coordinates if not included in the profile.
    """

    # Step 1: Insert user into SQL (auto-generates user_id)
    user_id = insert_customer((user_data["name"], user_data["email"]))

    # Step 2: Prepare MongoDB profile data
    profile_doc = profile_template or {
        "preferred_categories": [],
        "avg_rating_given": 0.0,
        "address": {
            "street": "",
            "city": "",
            "state": "",
            "zip": "",
            "country": ""
        }
    }

    # Assign the generated user_id to profile
    profile_doc["user_id"] = user_id

    # Step 3: Auto-fetch coordinates if missing
    if "coordinates" not in profile_doc:
        coords = geocode_address(profile_doc["address"])
        profile_doc["coordinates"] = {
            "type": "Point",
            "coordinates": coords
        }

    # Step 4: Insert profile into MongoDB
    add_profile(profile_doc)

    return {
    "status": "created",
    "user_id": user_id,
    "profile": profile_doc
}

def get_full_user_profile(user_id):
    sql_user = get_customer_by_id(user_id)
    mongo_profile = get_profile_by_user(user_id)

    if not sql_user or not mongo_profile:
        return None

    return {
        "user_id": user_id,
        "name": sql_user[1],
        "email": sql_user[2],
        "address": mongo_profile.get("address", {}),
        "coordinates": mongo_profile.get("coordinates", {}).get("coordinates", []),
        "preferred_categories": mongo_profile.get("preferred_categories", []),
        "avg_rating_given": mongo_profile.get("avg_rating_given", 0.0)
    }

def get_all_customer_locations():
    results = []
    for profile in db["customer_profiles"].find({}, {"user_id": 1, "coordinates": 1, "address": 1}):
        coords = profile.get("coordinates", {}).get("coordinates", [])
        if coords and len(coords) == 2:
            customer = get_customer_by_id(profile["user_id"])  # Fetch from SQL
            results.append({
                "user_id": profile["user_id"],
                "lat": coords[1],
                "lon": coords[0],
                "name": customer[1] if customer else "Unknown",
                "email": customer[2] if customer else "Unknown",
                "address": profile.get("address", {})
            })
    return results

def get_rating_customer_locations(min_rating=0.0, max_rating=5.0):
    """
    Returns customer locations with avg_rating_given in the given range.
    Default range includes all customers (0.0 to 5.0).
    """
    results = []

    # Build query with rating range and coordinates
    query = {
        "coordinates": {"$exists": True},
        "avg_rating_given": {"$gte": min_rating, "$lt": max_rating}
    }

    projection = {
        "user_id": 1,
        "coordinates": 1,
        "address": 1,
        "avg_rating_given": 1
    }

    for profile in db["customer_profiles"].find(query, projection):
        coords = profile.get("coordinates", {}).get("coordinates", [])
        if coords and len(coords) == 2:
            customer = get_customer_by_id(profile["user_id"])
            results.append({
                "user_id": profile["user_id"],
                "lat": coords[1],
                "lon": coords[0],
                "name": customer[1] if customer else "Unknown",
                "email": customer[2] if customer else "Unknown",
                "address": profile.get("address", {}),
                "avg_rating_given": profile.get("avg_rating_given", 0.0)
            })

    return results

from pymongo import GEOSPHERE
from math import radians

def get_users_near_location(center_coords, max_distance_km):
    """
    Finds users within max_distance_km from a given center [lon, lat].
    Returns user_id, name, email, coordinates, and distance.
    """

    # Convert distance to meters
    max_distance_meters = max_distance_km * 1000

    # Make sure the collection is indexed for geo queries
    db.customer_profiles.create_index([("coordinates", GEOSPHERE)])

    results = []
    for profile in db.customer_profiles.find({
        "coordinates": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": center_coords
                },
                "$maxDistance": max_distance_meters
            }
        }
    }):
        coords = profile["coordinates"]["coordinates"]
        customer = get_customer_by_id(profile["user_id"])
        results.append({
            "user_id": profile["user_id"],
            "lat": coords[1],
            "lon": coords[0],
            "name": customer[1] if customer else "Unknown",
            "email": customer[2] if customer else "Unknown",
            "address": profile.get("address", {}),
            "avg_rating_given": profile.get("avg_rating_given", 0.0)
        })

    return results

