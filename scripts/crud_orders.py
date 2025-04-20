import sqlite3

DB_PATH = "db/sql/hybrid_bookstore.db"

def get_all_orders():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM orders").fetchall()

def get_orders_by_user(user_id):
    with sqlite3.connect("db/sql/hybrid_bookstore.db") as conn:
        return conn.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,)).fetchall()

def get_order_by_id(order_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchone()

def insert_order(order_data):  # order_data = (user_id, order_date, total_amount, total_items)
    with sqlite3.connect(DB_PATH) as conn:
        cursor=conn.execute(
            "INSERT INTO orders (user_id, order_date, total_amount, total_items) VALUES (?, ?, ?, ?)", order_data)
        conn.commit()
        return cursor.lastrowid # returns the auto-generated order_id


def insert_order_detail(order_detail):  # order_detail = (order_id, book_id, quantity, unit_price)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO order_details (order_id, book_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
            order_detail
        )
        conn.commit()

def get_order_details(order_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM order_details WHERE order_id = ?", (order_id,)).fetchall()

def delete_order_details_for_order(order_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM order_details WHERE order_id = ?", (order_id,))
        conn.commit()

def delete_order(order_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        conn.commit()

def delete_full_order(order_id):
    """Deletes order details first, then the order itself."""
    delete_order_details_for_order(order_id)
    delete_order(order_id)
