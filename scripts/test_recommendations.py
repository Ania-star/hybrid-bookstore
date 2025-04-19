import crud_recommendations as rc

print("\nTesting Recommendations Collection")

rec_doc = {
    "user_id": 1001,
    "recommended_books": ["BKS-000008", "BKS-000009"]
}

# Create
print("Add recommendation:")
print(rc.add_recommendation(rec_doc))

# Read
print("Get recommendations by user:")
print(rc.get_recommendations_by_user(1001))

# Update
print("Update recommended books:")
print(rc.update_recommendations(1001, ["BKS-000010", "BKS-000011"]))

# Delete
print("Delete recommendation:")
print(rc.delete_recommendation(1001))
