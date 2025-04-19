import crud_browsing_history as bh

print("\nTesting Browsing History Collection")

entry = {
    "user_id": 1001,
    "book_id": "BKS-000007",
    "timestamp": "2025-04-19T21:00:00Z"
}

# Create
print("Add entry:")
print(bh.add_history_entry(entry))

# Read
print("Get history by user:")
for h in bh.get_history_by_user(1001):
    print(h)

# Delete
print("Delete entry:")
print(bh.delete_history_entry(1001, "BKS-000007"))
