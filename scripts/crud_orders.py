
import sqlite3

DB_PATH = "db/sql/hybrid_bookstore.db"

def get_all_orders():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM orders").fetchall()

def get_order_by_id(order_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchone()

def insert_order(order):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO orders (order_id, user_id, order_date, total_amount, total_items) VALUES (?, ?, ?, ?, ?)", order)
        conn.commit()

def insert_order_detail(order_detail):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO order_details (order_id, book_id, quantity, unit_price) VALUES (?, ?, ?, ?)", order_detail)
        conn.commit()

def get_order_details(order_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM order_details WHERE order_id = ?", (order_id,)).fetchall()
