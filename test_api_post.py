
from transaction_test_data import TRANSACTION_TEST_CASES
import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_create_transaction_returns_201():

    payload = {
        "title": "Banking transaction",
        "body": "Payment of 125.50 GBP",
        "userId": 1
    }

    response = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        timeout=10
    )

    assert response.status_code == 201


def test_created_transaction_returns_correct_data():

    payload = {
        "title": "Banking transaction",
        "body": "Payment of 125.50 GBP",
        "userId": 1
    }

    response = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        timeout=10
    )

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert "id" in data


def test_api_response_when_title_is_missing():

    payload = {
        "body": "Payment of 125.50 GBP",
        "userId": 1
    }

    response = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        timeout=10
    )

    data = response.json()

    assert response.status_code == 201
    assert "title" not in data


def test_api_response_when_amount_is_negative():

    payload = {
        "title": "Banking transaction",
        "body": "Payment of -125.50 GBP",
        "userId": 1
    }

    response = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        timeout=10
    )

    data = response.json()

    assert response.status_code == 201
    assert data["body"] == "Payment of -125.50 GBP"


@pytest.mark.parametrize(
    "test_case",
    TRANSACTION_TEST_CASES,
    ids=lambda case: case["description"]
)
def test_create_transaction_with_different_amounts(test_case):

    amount = test_case["amount"]

    payload = {
        "title": "Banking transaction",
        "body": f"Payment of {amount} GBP",
        "userId": 1
    }

    response = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        timeout=10
    )

    data = response.json()

    assert response.status_code == 201
    assert data["body"] == f"Payment of {amount} GBP"
