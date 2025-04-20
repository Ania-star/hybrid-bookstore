from crud_customers import (
    insert_customer,
    get_all_customers,
    get_customer_by_id,
    update_customer_email,
    delete_customer
)

print("\n Testing CRUD - SQL Customers")

# Insert
insert_customer((9999, "Test User", "test@example.com"))

# Read all
print("All customers:")
for row in get_all_customers():
    print(row)

# Read one
print("\nGet user_id 9999:")
print(get_customer_by_id(9999))

# Update
print("\nUpdate email for 9999:")
update_customer_email(9999, "new_email@example.com")
print(get_customer_by_id(9999))

# Delete
print("\nDelete user_id 9999:")
delete_customer(9999)
print("After deletion:", get_customer_by_id(9999))
