
import sqlite3


DB_PATH = "db/sql/hybrid_bookstore.db"

def get_all_customers():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM customers").fetchall()

def get_customer_by_id(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM customers WHERE user_id = ?", (user_id,)).fetchone()

def insert_customer(customer):  # customer = (name, email)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("INSERT INTO customers (name, email) VALUES (?, ?)", customer)
        conn.commit()
        return cursor.lastrowid  # returns the auto-generated user_id

def update_customer_email(user_id, new_email):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE customers SET email = ? WHERE user_id = ?", (new_email, user_id))
        conn.commit()

def delete_customer(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM customers WHERE user_id = ?", (user_id,))
        conn.commit()
