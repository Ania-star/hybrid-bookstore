import sqlite3
import pandas as pd

# Path to your SQLite database
db_path = r"C:\Users\annab\OneDrive - purdue.edu\NoSQL\Final Report\Git\hybrid-bookstore\db\sql\hybrid_bookstore.db"

# Connect to the database
conn = sqlite3.connect(db_path)

# Read the first few rows from the books table
try:
    df = pd.read_sql_query("SELECT * FROM books LIMIT 10", conn)
    print("Preview of books in the database:")
    print(df)
except Exception as e:
    print("Failed to query books table:", e)

conn.close()
