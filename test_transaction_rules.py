import sqlite3
import pytest

from config.settings import DATABASE_NAME
from config.api_client import create_transaction

@pytest.fixture(autouse=True)
def clean_transaction_test_data():

    connection = sqlite3.connect(DATABASE_NAME)

    try:
        test_ids = ("TXN4001", "TXN4002", "TXN4003", "TXN4004","TXN4005","TXN4006","TXN4007","TXN4008","TXN4009","TXN4010","TXN4011","TXN4012")

        connection.execute(
            "DELETE FROM transactions WHERE transaction_id IN (?, ?, ?, ? ,?,?,?,?,?,?,?,?)",
            test_ids
        )

        connection.commit()

    finally:
        connection.close()

def test_valid_transaction():

    payload = {
        "transaction_id": "TXN4001",
        "amount": 100.00,
        "account_reference": "ACC4001"
    }

    response = create_transaction(payload)

    assert response.status_code == 201
    assert response.json()["transaction_id"] == "TXN4001"

def test_minimum_transaction_amount():

    payload = {
        "transaction_id": "TXN4002",
        "amount": 0.01,
        "account_reference": "ACC4001"
    }

    response = create_transaction(payload)

    assert response.status_code == 201
    assert response.json()["transaction_id"] == "TXN4002"

def test_transaction_above_maximum_is_rejected():

    payload = {
        "transaction_id": "TXN4003",
        "amount": 5000.01,
        "account_reference": "ACC4003"
    }

    response = create_transaction(payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Amount exceeds maximum limit"

def test_maximum_transaction_amount():

    payload = {
        "transaction_id": "TXN4004",
        "amount": 5000.00,
        "account_reference": "ACC4004"
    }

    response = create_transaction(payload)

    assert response.status_code == 201
    assert response.json()["transaction_id"] == "TXN4004"

def test_transaction_just_below_maximum():

    payload = {
        "transaction_id": "TXN4005",
        "amount": 4999.99,
        "account_reference": "ACC4005"
    }

    response = create_transaction(payload)

    assert response.status_code == 201
    assert response.json()["transaction_id"] == "TXN4005"

def test_zero_amount_is_rejected():

    payload = {
        "transaction_id": "TXN4006",
        "amount": 0.00,
        "account_reference": "ACC4006"
    }

    response = create_transaction(payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Amount must be positive"

def test_negative_amount_is_rejected():

    payload = {
        "transaction_id": "TXN4007",
        "amount": -10.00,
        "account_reference": "ACC4007"
    }

    response = create_transaction(payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Amount must be positive"

def test_inactive_account_is_rejected():

    payload = {
        "transaction_id": "TXN4008",
        "amount": 100.00,
        "account_reference": "ACC4002"
    }

    response = create_transaction(payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Account is inactive"

def test_unknown_account_is_rejected():

    payload = {
        "transaction_id": "TXN4009",
        "amount": 100.00,
        "account_reference": "ACC9999"
    }

    response = create_transaction(payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Account is inactive"

def test_insufficient_funds_is_rejected():

    payload = {
        "transaction_id": "TXN4010",
        "amount": 1500.00,
        "account_reference": "ACC4001"
    }

    response = create_transaction(payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Insufficient funds"

def test_transaction_using_exact_available_balance():

    payload = {
        "transaction_id": "TXN4011",
        "amount": 1000.00,
        "account_reference": "ACC4001"
    }

    response = create_transaction(payload)

    assert response.status_code == 201
    assert response.json()["transaction_id"] == "TXN4011"

def test_inactive_account_with_excessive_amount():

    payload = {
        "transaction_id": "TXN4012",
        "amount": 6000.00,
        "account_reference": "ACC4002"
    }

    response = create_transaction(payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Amount exceeds maximum limit"