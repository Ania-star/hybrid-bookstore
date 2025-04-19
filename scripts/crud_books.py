
import sqlite3

DB_PATH = "db/sql/hybrid_bookstore.db"

def get_all_books():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM books").fetchall()

def get_book_by_id(book_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM books WHERE book_id = ?", (book_id,)).fetchone()

def insert_book(book):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO books (book_id, title, category_id, star_rating, price, status, quantity) VALUES (?, ?, ?, ?, ?, ?, ?)", book)
        conn.commit()

def update_book_quantity(book_id, quantity):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (quantity, book_id))
        conn.commit()

def delete_book(book_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        conn.commit()
