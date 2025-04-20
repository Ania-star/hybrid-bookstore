from integration_reviews import submit_review

# Test: Submit a review for book BKS-000002 by user 1
print("Submitting review...")
review = submit_review(1, "BKS-000002", 5, "Amazing book! Learned a lot.")
print("Review submitted:", review)
