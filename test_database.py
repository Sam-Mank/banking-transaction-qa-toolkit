
import sqlite3


def get_transactions():

    connection = sqlite3.connect("banking_qa.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT transaction_id, amount, status
    FROM transactions
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def test_database_contains_five_transactions():

    transactions = get_transactions()

    assert len(transactions) == 5


def test_approved_transaction_exists():

    transactions = get_transactions()

    approved = [
        transaction for transaction in transactions
        if transaction[2] == "APPROVED"
    ]

    assert len(approved) == 3


def test_declined_transaction_exists():

    transactions = get_transactions()

    declined = [
        transaction for transaction in transactions
        if transaction[2] == "DECLINED"
    ]

    assert len(declined) == 1


def test_pending_transaction_exists():

    transactions = get_transactions()

    pending = [
        transaction for transaction in transactions
        if transaction[2] == "PENDING"
    ]

    assert len(pending) == 1


def test_transaction_amount_is_correct():

    transactions = get_transactions()

    transaction = [
        item for item in transactions
        if item[0] == "TXN2001"
    ]

    assert len(transaction) == 1
    assert transaction[0][1] == 25.50


def test_all_transaction_amounts_are_positive():

    transactions = get_transactions()

    for transaction in transactions:
        assert transaction[1] > 0


def test_all_transactions_have_account_references():

    connection = sqlite3.connect("banking_qa.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT account_reference
    FROM transactions
    """)

    results = cursor.fetchall()
    connection.close()

    for result in results:
        assert result[0] is not None
        assert result[0] != ""
