
import sqlite3

connection = sqlite3.connect("banking_qa.db")
cursor = connection.cursor()

cursor.execute("""
SELECT transaction_id, amount, status, account_reference
FROM transactions
WHERE transaction_id = ?
""", ("TXN3001",))

transaction = cursor.fetchone()

connection.close()

print("\nDATABASE VERIFICATION")
print("=====================")

if transaction:
    print("Transaction found:")
    print(transaction)
else:
    print("FAIL - Transaction not found in database")
