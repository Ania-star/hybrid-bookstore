from scripts.crud_books import get_book_by_id
from scripts.crud_categories import get_category_by_id

def get_book_with_category(book_id):
    """
    Retrieves book information and joins it with the category name.
    Returns a dictionary with combined details.
    """
    book = get_book_by_id(book_id)
    if not book:
        return None

    book_id, title, category_id, star_rating, price, status, quantity = book
    category = get_category_by_id(category_id)
    category_name = category[1] if category else "Unknown"

    return {
        "book_id": book_id,
        "title": title,
        "category_id": category_id,
        "category_name": category_name,
        "star_rating": star_rating,
        "price": price,
        "status": status,
        "quantity": quantity
    }
