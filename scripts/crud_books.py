
import sqlite3

DB_PATH = "db/sql/hybrid_bookstore.db"

def get_next_book_id():
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT book_id FROM books ORDER BY book_id DESC LIMIT 1").fetchone()
        if result:
            last_id = result[0]
            num = int(last_id.split("-")[1])
            return f"BKS-{str(num + 1).zfill(6)}"
        else:
            return "BKS-000001"

def get_all_books():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM books").fetchall()
    
def get_books_by_category(category_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM books WHERE category_id = ?", (category_id,)).fetchall()

def get_book_by_id(book_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM books WHERE book_id = ?", (book_id,)).fetchone()

def insert_book(book_data):  # book_data = (title, category_id, star_rating, price, status, quantity)
    book_id = get_next_book_id()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO books (book_id, title, category_id, rating, price, status, quantity) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (book_id, *book_data)
        )
        conn.commit()
    return book_id  # to use it later

def update_book_quantity(book_id, quantity):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (quantity, book_id))
        conn.commit()

def delete_book(book_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        conn.commit()

def update_book_rating(book_id, new_avg_rating):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE books SET rating = ? WHERE book_id = ?", (new_avg_rating, book_id))
        conn.commit()

