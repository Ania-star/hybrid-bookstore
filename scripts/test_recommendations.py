import crud_recommendations as rc
from pprint import pprint

print("\nTesting Recommendations Collection")

rec_doc = {
    "user_id": 1,
    "recommended_books": ["BKS-000008", "BKS-000009"]
}

# Create or update
print("Add recommendation:")
pprint(rc.update_recommendations(rec_doc["user_id"], rec_doc["recommended_books"]))

# Read
print("Get recommendations by user:")
pprint(rc.get_recommendations_by_user(1001))

# Update
print("Update recommended books:")
pprint(rc.update_recommendations(1001, ["BKS-000010", "BKS-000011"]))

# Delete
print("Delete recommendation:")
pprint(rc.delete_recommendation(1001))
