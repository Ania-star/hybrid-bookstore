
-- Table: categories
CREATE TABLE IF NOT EXISTS categories (
    category_id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Table: books
CREATE TABLE IF NOT EXISTS books (
    book_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category_id TEXT NOT NULL,
    rating REAL,
    price REAL NOT NULL,
    status TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Table: customers
CREATE TABLE IF NOT EXISTS customers (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Table: orders
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    total_amount REAL NOT NULL,
    total_items INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES customers(user_id)
);

-- Table: order_details
CREATE TABLE IF NOT EXISTS order_details (
    order_id TEXT NOT NULL,
    book_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    PRIMARY KEY (order_id, book_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);
