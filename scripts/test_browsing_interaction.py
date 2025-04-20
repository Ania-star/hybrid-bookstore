from integration_browsing import log_and_get_book  

user_id = 1
book_id = "BKS-000002"

print(f"Logging interaction and retrieving book details for user {user_id} and book {book_id}...")
book = log_and_get_book(user_id, book_id)

print("Book details returned:")
print(book)
