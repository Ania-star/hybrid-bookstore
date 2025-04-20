from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime
from scripts.integration_recommendations import generate_recommendations



load_dotenv()

from scripts.crud_orders import (
    insert_order,
    insert_order_detail,
    get_order_details,
)
from scripts.crud_customers import get_customer_by_id
from scripts.crud_books import get_book_by_id, update_book_quantity
from scripts.crud_books import get_book_by_id

# DB_PATH
DB_PATH = "db/sql/hybrid_bookstore.db"

def create_order_with_details(user_id, books):
    """
    Places an order for a user, including multiple books.
    Each book entry must contain 'book_id' and 'quantity'.
    """

    # Step 1: Validate user
    user = get_customer_by_id(user_id)
    if not user:
        raise ValueError(f"User {user_id} does not exist.")

    total_amount = 0.0
    total_items = 0
    order_details = []
    stock_updates = []  # store update instructions until confirmed

    # Step 2: Validate books and calculate totals
    for item in books:
        book = get_book_by_id(item["book_id"])
        if not book:
            raise ValueError(f"Book {item['book_id']} does not exist.")

        quantity = item["quantity"]
        price = book[4]
        available = book[6]

        if quantity > available:
            raise ValueError(f"Not enough stock for {item['book_id']} (requested {quantity}, available {available})")

        total_amount += price * quantity
        total_items += quantity

        order_details.append({
            "book_id": item["book_id"],
            "quantity": quantity,
            "unit_price": price
        })

        stock_updates.append((item["book_id"], available - quantity))

    # Step 3: Insert order
    order_date = datetime.now().isoformat()
    order_id = insert_order((user_id, order_date, total_amount, total_items))

    # Step 4: Insert order details
    for detail in order_details:
        insert_order_detail((order_id, detail["book_id"], detail["quantity"], detail["unit_price"]))

    # Step 5: Now reduce stock — after order is confirmed
    for book_id, new_quantity in stock_updates:
        update_book_quantity(book_id, new_quantity)

    return {
        "status": "success",
        "order_id": order_id,
        "total_amount": round(total_amount, 2),
        "total_items": total_items,
        "date": order_date
    }


def delete_order_details_for_order(order_id):
    """
    Deletes all order detail rows for a given order.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM order_details WHERE order_id = ?", (order_id,))
        conn.commit()



def update_order_details(order_id, new_items):
    """
    Replaces the order_details for a given order_id.
    Expects new_items = [{"book_id": ..., "quantity": ...}]
    Unit price is pulled from the books table.
    """
    delete_order_details_for_order(order_id)

    for item in new_items:
        book = get_book_by_id(item["book_id"])
        if not book:
            raise ValueError(f"Book {item['book_id']} not found.")

        unit_price = book[4]  
        insert_order_detail((order_id, item["book_id"], item["quantity"], unit_price))
    

    return get_order_details(order_id)


def delete_order(order_id):
    """
    Deletes an entire order and its associated details.
    """
    delete_order_details_for_order(order_id)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        conn.commit()

def update_order_summary(order_id):
    """
    Recalculates and updates total_items, total_amount, and order_date
    after order details are modified.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT SUM(quantity), SUM(quantity * unit_price) FROM order_details WHERE order_id = ?",
            (order_id,)
        )
        total_items, total_amount = cursor.fetchone()

        if total_items is None or total_amount is None:
            total_items, total_amount = 0, 0.0

        order_date = datetime.now().isoformat()

        conn.execute(
            "UPDATE orders SET total_items = ?, total_amount = ?, order_date = ? WHERE order_id = ?",
            (total_items, total_amount, order_date, order_id)
        )
        conn.commit()


