
from flask import Flask, request, jsonify
import sqlite3

from config.settings import DATABASE_NAME

app = Flask(__name__)

DATABASE = DATABASE_NAME

# Fictional account test data
ACCOUNT_STATUSES = {
    "ACC4001": "ACTIVE",
    "ACC4002": "INACTIVE",
    "ACC4003": "ACTIVE",
    "ACC4004": "ACTIVE",
    "ACC4005": "ACTIVE",
    "ACC4006": "ACTIVE",
    "ACC4007": "ACTIVE",
    "ACC4008": "INACTIVE",
    "ACC2001": "ACTIVE",
    "ACC2002": "ACTIVE"
}
# Fictional account balances
ACCOUNT_BALANCES = {
    "ACC4001": 1000.00,
    "ACC4002": 1000.00,
    "ACC4003": 1000.00,
    "ACC4004": 10000.00,
    "ACC4005": 10000.00,
    "ACC4006": 1000.00,
    "ACC4007": 1000.00,
    "ACC4008": 1000.00,
    "ACC2001": 1000.00,
    "ACC2002": 1000.00
}

def save_transaction(transaction_id, amount, status, account_reference):

    connection = sqlite3.connect(DATABASE)

    try:
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO transactions
        (transaction_id, amount, status, account_reference)
        VALUES (?, ?, ?, ?)
        """, (transaction_id, amount, status, account_reference))

        connection.commit()

    finally:
        connection.close()


@app.route("/transactions", methods=["POST"])
def create_transaction():

    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required_fields = [
        "transaction_id",
        "amount",
        "account_reference"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400

    if amount > 5000:
        return jsonify({"error": "Amount exceeds maximum limit"}), 400
    
    account_reference = data["account_reference"]

    account_status = ACCOUNT_STATUSES.get(account_reference)

    if account_status != "ACTIVE":
        return jsonify({"error": "Account is inactive"}), 400
    
    available_balance = ACCOUNT_BALANCES.get(account_reference)

    if available_balance is None:
        return jsonify({"error": "Account balance not found"}), 400

    if amount > available_balance:
        return jsonify({"error": "Insufficient funds"}), 400

    try:
        save_transaction(
            data["transaction_id"],
            amount,
            "APPROVED",
            data["account_reference"]
        )

    except sqlite3.IntegrityError:
        return jsonify({"error": "Duplicate transaction ID"}), 409

    return jsonify({
        "transaction_id": data["transaction_id"],
        "amount": amount,
        "status": "APPROVED",
        "account_reference": data["account_reference"]
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
