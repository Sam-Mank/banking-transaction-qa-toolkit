
import requests
import sqlite3
import pytest

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture(autouse=True)
def clean_test_transactions():

    connection = sqlite3.connect("banking_qa.db")

    test_ids = (
        "TXN3001",
        "TXN3002",
        "TXN3003",
        "TXN3004"
    )

    placeholders = ",".join("?" for _ in test_ids)

    connection.execute(
        f"DELETE FROM transactions WHERE transaction_id IN ({placeholders})",
        test_ids
    )

    connection.commit()
    connection.close()


def test_create_transaction_successfully():

    payload = {
        "transaction_id": "TXN3002",
        "amount": 75.00,
        "account_reference": "ACC2002"
    }

    response = requests.post(
        f"{BASE_URL}/transactions",
        json=payload,
        timeout=10
    )

    assert response.status_code == 201
    assert response.json()["transaction_id"] == "TXN3002"



def test_duplicate_transaction_is_rejected():

    payload = {
        "transaction_id": "TXN3001",
        "amount": 125.50,
        "account_reference": "ACC2001"
    }

    # First submission should succeed
    first_response = requests.post(
        f"{BASE_URL}/transactions",
        json=payload,
        timeout=10
    )

    assert first_response.status_code == 201

    # Second submission should be rejected
    second_response = requests.post(
        f"{BASE_URL}/transactions",
        json=payload,
        timeout=10
    )

    assert second_response.status_code == 409
    assert second_response.json()["error"] == "Duplicate transaction ID"



def test_negative_transaction_amount_is_rejected():

    payload = {
        "transaction_id": "TXN3003",
        "amount": -50.00,
        "account_reference": "ACC2003"
    }

    response = requests.post(
        f"{BASE_URL}/transactions",
        json=payload,
        timeout=10
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Amount must be positive"


def test_missing_transaction_id_is_rejected():

    payload = {
        "amount": 50.00,
        "account_reference": "ACC2004"
    }

    response = requests.post(
        f"{BASE_URL}/transactions",
        json=payload,
        timeout=10
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing field: transaction_id"


def test_invalid_amount_format_is_rejected():

    payload = {
        "transaction_id": "TXN3004",
        "amount": "invalid",
        "account_reference": "ACC2005"
    }

    response = requests.post(
        f"{BASE_URL}/transactions",
        json=payload,
        timeout=10
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Invalid amount"
