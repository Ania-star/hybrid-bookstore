from integration_books import get_book_with_category

book_id = "BKS-000002"
book = get_book_with_category(book_id)

if book:
    print("Book with category:")
    for k, v in book.items():
        print(f"{k}: {v}")
else:
    print("Book not found.")
