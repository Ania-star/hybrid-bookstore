
import sqlite3

DB_PATH = "db/sql/hybrid_bookstore.db"

def get_all_categories():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM categories").fetchall()

def get_category_by_id(category_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM categories WHERE category_id = ?", (category_id,)).fetchone()

def insert_category(category):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO categories (category_id, name) VALUES (?, ?)", category)
        conn.commit()

def update_category_name(category_id, new_name):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE categories SET name = ? WHERE category_id = ?", (new_name, category_id))
        conn.commit()
