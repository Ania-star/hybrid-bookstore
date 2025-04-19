
import pandas as pd
import sqlite3
import os

print("Script started")
# Paths to your CSV files
csv_files = {
    "categories": "data/categories.csv",
    "customers": "data/customers.csv",
    "orders": "data/orders.csv",
    "order_details": "data/order_details.csv",
    "books": "data/books.csv"
}

# SQLite DB path
db_path = r"C:\Users\annab\OneDrive - purdue.edu\NoSQL\Final Report\Git\hybrid-bookstore\db\sql\hybrid_bookstore.db"

# Connect to SQLite
conn = sqlite3.connect(db_path)

# Load and insert each CSV
for table, path in csv_files.items():
    print(f"Checking {table} at: {path}")
    if not os.path.exists(path):
        print(f"File not found for {table}: {path}")
        continue

    try:
        df = pd.read_csv(path)
        print(f"Loaded {len(df)} rows for table: {table}")
        print(df.head())
        df.to_sql(table, conn, if_exists="append", index=False)
        print(f"Inserted data into {table} table.\n")
    except Exception as e:
        print(f"Failed to process {table}: {e}\n")

conn.commit()
conn.close()
input("All done. Press Enter to close...")
