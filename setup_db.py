import sqlite3

conn = sqlite3.connect("store.db")
cursor = conn.cursor()

# Enforce foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Reset tables
cursor.execute("DROP TABLE IF EXISTS orders;")
cursor.execute("DROP TABLE IF EXISTS customers;")

# 1. Customers table
cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL
);
""")

# 2. Orders table with relational integrity
cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
""")

# 3. Seed baseline data
cursor.executemany(
    "INSERT INTO customers (customer_id, first_name) VALUES (?, ?);",
    [(1, "Abebe"), (2, "Helen")]
)

cursor.executemany(
    "INSERT INTO orders (customer_id, order_date, amount, status) VALUES (?, ?, ?, ?);",
    [
        (1, "2026-10-10", 45.50, "Delivered"),
        (1, "2026-10-12", 120.00, "Shipped"),
    ]
)

conn.commit()
conn.close()
print("store.db cleanly reset and seeded!")