from integration_ut import create_user_with_profile

print("\nTesting create_user_with_profile")

user_data = {
    "name": "GeoUser Example",
    "email": "geo.user@example.com"
}

profile = {
    "preferred_categories": ["Fantasy", "Adventure"],
    "avg_rating_given": 4.7,
    "address": {
        "street": "610 Purdue Mall",
        "city": "West Lafayette",
        "state": "IN",
        "country": "USA"
    }
    # coordinates will be auto-generated
}

result = create_user_with_profile(user_data, profile)
print("Result:", result)
