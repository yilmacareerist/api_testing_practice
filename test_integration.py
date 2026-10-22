import sqlite3
import pytest

def api_create_order(payload: dict, db_path="store.db") -> dict:
    required_keys = {"customer_id", "order_date", "amount", "status"}
    if not required_keys.issubset(payload.keys()):
        return {"status_code": 400, "error": "Missing required fields"}

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    try:
        cursor.execute(
            """
            INSERT INTO orders (customer_id, order_date, amount, status)
            VALUES (?, ?, ?, ?);
            """,
            (
                payload["customer_id"],
                payload["order_date"],
                payload["amount"],
                payload["status"],
            ),
        )
        conn.commit()
        order_id = cursor.lastrowid
        return {
            "status_code": 201,
            "data": {
                "order_id": order_id,
                "customer_id": payload["customer_id"],
                "amount": payload["amount"],
                "status": payload["status"],
            },
        }
    except sqlite3.IntegrityError as e:
        return {"status_code": 422, "error": str(e)}
    finally:
        conn.close()

def test_api_post_order_persists_to_database():
    request_payload = {
        "customer_id": 1,
        "order_date": "2026-10-22",
        "amount": 129.50,
        "status": "Completed",
    }

    response = api_create_order(request_payload)
    assert response["status_code"] == 201
    created_id = response["data"]["order_id"]
    assert created_id is not None

    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT customer_id, order_date, amount, status FROM orders WHERE order_id = ?;",
        (created_id,),
    )
    row = cursor.fetchone()
    conn.close()

    assert row is not None, f"Order {created_id} was not found in store.db!"
    assert row[0] == request_payload["customer_id"]
    assert row[1] == request_payload["order_date"]
    assert row[2] == request_payload["amount"]
    assert row[3] == request_payload["status"]
