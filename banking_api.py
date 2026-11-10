
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "banking_qa.db"


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
