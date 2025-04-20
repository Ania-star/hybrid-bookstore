from datetime import datetime
from scripts.crud_books import get_book_by_id
from scripts.crud_browsing_history import add_history_entry

def log_and_get_book(user_id, book_id):
    """
    Logs the user's book interaction and returns book details.
    """
    # Step 1: Log interaction
    entry = {
        "user_id": user_id,
        "book_id": book_id,
        "timestamp": datetime.utcnow().isoformat()
    }
    add_history_entry(entry)

    # Step 2: Return book details from SQL
    return get_book_by_id(book_id)
