import crud_reviews as rv

print("\nTesting Reviews Collection")

review = {
    "user_id": 1001,
    "book_id": "BKS-000006",
    "rating": 5,
    "review_text": "One of the best reads ever!",
    "timestamp": "2025-04-19T20:00:00Z"
}

# Add a review
print("Add review:")
print(rv.add_review(review))

# Get all reviews by user_id
print("Get reviews by user 1001:")
for r in rv.get_reviews_by_user(1001):
    print(r)

# Update rating
print("Update rating to 4:")
print(rv.update_review_rating(1001, "BKS-000006", 4))

# Get all reviews by book_id
print("Get reviews for book_id BKS-000006:")
for r in rv.get_reviews_by_book("BKS-000006"):
    print(r)

# Delete review
print("Delete review:")
print(rv.delete_review(1001, "BKS-000006"))
