import sqlite3

DB_PATH = "db/sql/hybrid_bookstore.db"

def get_next_category_id():
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT category_id FROM categories ORDER BY category_id DESC LIMIT 1").fetchone()
        if result:
            last_id = result[0]
            num = int(last_id.split("-")[1])
            return f"CAT-{str(num + 1).zfill(6)}"
        else:
            return "CAT-000001"

def get_all_categories():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM categories").fetchall()

def get_category_by_id(category_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM categories WHERE category_id = ?", (category_id,)).fetchone()

def insert_category(category_name):  # Just the name
    category_id = get_next_category_id()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO categories (category_id, name) VALUES (?, ?)", (category_id, category_name))
        conn.commit()
    return category_id

def update_category_name(category_id, new_name):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE categories SET name = ? WHERE category_id = ?", (new_name, category_id))
        conn.commit()
