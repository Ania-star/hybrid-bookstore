import os
from dotenv import load_dotenv
import requests  # Used for calling Google Maps API

from crud_customers import insert_customer  # SQL helper
from crud_customer_profiles import add_profile  # MongoDB helper

# Load .env environment variables (like your Google API key)
load_dotenv()

# You no longer need Nominatim since you switched to Google Maps


def geocode_address(address_dict):
    """Converts address fields to coordinates using Google Maps API"""
    address_str = ", ".join([v for v in address_dict.values() if v])
    print("📍 Geocoding address (Google):", address_str)

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

    return {"status": "created", "user_id": user_id}


