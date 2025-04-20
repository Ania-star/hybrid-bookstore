from integration_orders import (
    create_order_with_details,
    update_order_details,
    delete_order,
)
from crud_orders import get_order_details

# --- Step 1: CREATE Order ---
print("Creating new order...")
order = create_order_with_details(1, [
    {"book_id": "BKS-000002", "quantity": 1},
    {"book_id": "BKS-000009", "quantity": 2}
])
print("Order created:", order)

order_id = order["order_id"]

# --- Step 2: UPDATE Order ---
#print("\n Updating order details...")
#updated_details = update_order_details(order_id, [
#    {"book_id": "BKS-000002", "quantity": 2},  
#    {"book_id": "BKS-000004", "quantity": 1}   
#])#
#print("Order updated. New details:")
#for row in updated_details:
#    print(row)

# --- Step 3: DELETE Order ---
#print("\nDeleting order...")
#delete_order(order_id)
#print(f"Order {order_id} deleted.")
