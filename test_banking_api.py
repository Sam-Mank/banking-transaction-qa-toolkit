
import sqlite3
import pytest

from config.settings import DATABASE_NAME
from config.api_client import create_transaction


@pytest.fixture(autouse=True)
def clean_test_transactions():

    connection = sqlite3.connect(DATABASE_NAME)

    try:
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

    finally:
        connection.close()


def test_create_transaction_successfully():

    payload = {
        "transaction_id": "TXN3002",
        "amount": 75.00,
        "account_reference": "ACC2002"
    }

    response = create_transaction(payload)

    assert response.status_code == 201
    assert response.json()["transaction_id"] == "TXN3002"



def test_duplicate_transaction_is_rejected():

    payload = {
        "transaction_id": "TXN3001",
        "amount": 125.50,
        "account_reference": "ACC2001"
    }

    # First submission should succeed
    first_response = create_transaction(payload)

    assert first_response.status_code == 201

    # Second submission should be rejected
    second_response = create_transaction(payload)

    assert second_response.status_code == 409
    assert second_response.json()["error"] == "Duplicate transaction ID"



def test_negative_transaction_amount_is_rejected():

    payload = {
        "transaction_id": "TXN3003",
        "amount": -50.00,
        "account_reference": "ACC2003"
    }

    response = create_transaction(payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Amount must be positive"


def test_missing_transaction_id_is_rejected():

    payload = {
        "amount": 50.00,
        "account_reference": "ACC2004"
    }

    response = create_transaction(payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Missing field: transaction_id"


def test_invalid_amount_format_is_rejected():

    payload = {
        "transaction_id": "TXN3004",
        "amount": "invalid",
        "account_reference": "ACC2005"
    }

    response = create_transaction(payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Invalid amount"
