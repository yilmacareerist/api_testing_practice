import sqlite3
import pytest

@pytest.fixture
def db_conn():
    conn = sqlite3.connect("store.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    yield conn
    conn.close()

@pytest.mark.parametrize("customer_name, expected_count", [
    ("Helen", 0),
    ("Abebe", 2),
])
def test_customer_order_counts(db_conn, customer_name, expected_count):
    cursor = db_conn.cursor()
    query = """
    SELECT COUNT(o.order_id)
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.first_name = ?;
    """
    cursor.execute(query, (customer_name,))
    count = cursor.fetchone()[0]
    
    assert count == expected_count, f"Expected {expected_count} orders for {customer_name}, but got {count}"

def test_foreign_key_prevents_orphan_orders(db_conn):
    cursor = db_conn.cursor()
    
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
            INSERT INTO orders (customer_id, order_date, amount, status)
            VALUES (9999, '2026-10-16', 150.00, 'Pending');
        """)

def test_customer_total_spend_aggregation(db_conn):
    cursor = db_conn.cursor()
    query = """
    SELECT c.first_name, SUM(o.amount)
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.first_name = 'Abebe'
    GROUP BY c.customer_id;
    """
    cursor.execute(query)
    row = cursor.fetchone()
    
    assert row is not None, "Expected customer Abebe to have order records"
    assert row[1] == 165.50, f"Expected total spend 165.50, but got {row[1]}"

def test_high_value_customers_having_clause(db_conn):
    cursor = db_conn.cursor()
    query = """
    SELECT c.first_name, SUM(o.amount) AS total_spent
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    HAVING total_spent > 100.00;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    assert len(rows) == 1, f"Expected 1 customer exceeding $100, found {len(rows)}"
    assert rows[0][0] == "Abebe"
def test_zero_spend_customer_returns_coalesce_default(db_conn):
    cursor = db_conn.cursor()
    query = """
    SELECT c.first_name, COALESCE(SUM(o.amount), 0.0) AS total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.first_name = 'Helen'
    GROUP BY c.customer_id;
    """
    cursor.execute(query)
    row = cursor.fetchone()

    assert row is not None, "Expected Helen record to exist in customers table"
    assert row[1] == 0.0, f"Expected total spend 0.0 for customer with no orders, but got {row[1]}"
def test_failed_transaction_triggers_rollback(db_conn):
    cursor = db_conn.cursor()

    # 1. Capture baseline order count
    cursor.execute("SELECT COUNT(*) FROM orders;")
    initial_count = cursor.fetchone()[0]

    # 2. Attempt a transaction where step 2 deliberately fails
    try:
        cursor.execute("BEGIN TRANSACTION;")
        # Valid insert
        cursor.execute(
            "INSERT INTO orders (customer_id, order_date, amount, status) VALUES (?, ?, ?, ?);",
            (1, "2026-10-21", 75.00, "Pending")
        )
        # Deliberate failure: customer_id 999 violates foreign key constraint
        cursor.execute(
            "INSERT INTO orders (customer_id, order_date, amount, status) VALUES (?, ?, ?, ?);",
            (999, "2026-10-21", 50.00, "Pending")
        )
        db_conn.commit()
    except Exception:
        # 3. Roll back all operations in the uncommitted transaction
        db_conn.rollback()

    # 4. Assert total orders count returned strictly to the baseline
    cursor.execute("SELECT COUNT(*) FROM orders;")
    final_count = cursor.fetchone()[0]

    assert final_count == initial_count, (
        f"Rollback failed: expected {initial_count} orders, but found {final_count}"
    )