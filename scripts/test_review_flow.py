from integration_reviews import get_books_to_review, submit_review

user_id = 1

books = get_books_to_review(user_id)

if not books:
    print("All books already reviewed.")
else:
    print("Books available to review:")
    for b in books:
        print("-", b)

    # Submit a review for the first unreviewed book
    book_id = books[0]
    print(f"\nSubmitting review for {book_id}...")
    result = submit_review(user_id, book_id, 5, "Insightful and enjoyable read!")
    print("Review submitted:", result)
