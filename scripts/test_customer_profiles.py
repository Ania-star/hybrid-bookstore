import crud_customer_profiles as cp

print("\nTesting Customer Profiles")

profile = {
    "user_id": 1001,
    "preferred_categories": ["Horror", "Fantasy"],
    "avg_rating_given": 4.3,
    "address": {
        "street": "789 Elm St",
        "city": "Indianapolis",
        "state": "IN",
        "zip": "46204",
        "country": "USA"
    },
    "coordinates": {
        "type": "Point",
        "coordinates": [-86.1581, 39.7684]
    }
}

# Create
print("Add profile:")
print(cp.add_profile(profile))

# Read
print("Get profile by user_id:")
print(cp.get_profile_by_user(1001))

# Update
print("Update avg_rating_given to 3.5:")
print(cp.update_profile_rating(1001, 3.5))

# GeoQuery
print("Find users near (-86.1600, 39.7700) within 5 km:")
users = cp.find_users_near(39.7700, -86.1600, 5)
for u in users:
    print(u)

# Delete
print("Delete user profile:")
print(cp.delete_profile(1001))
